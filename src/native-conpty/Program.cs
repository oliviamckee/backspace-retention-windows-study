using Microsoft.Win32.SafeHandles;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

internal static class Program
{
    private const uint ProcThreadAttributePseudoConsole = 0x00020016;
    private const uint ExtendedStartupInfoPresent = 0x00080000;
    private const int StdInputHandle = -10;
    private const int StdOutputHandle = -11;
    private const uint EnableProcessedInput = 0x0001;
    private const uint EnableLineInput = 0x0002;
    private const uint EnableEchoInput = 0x0004;
    private const uint EnableProcessedOutput = 0x0001;
    private const uint EnableVirtualTerminalProcessing = 0x0004;
    private const uint DisableNewlineAutoReturn = 0x0008;

    private static int Main(string[] args)
    {
        if (args.Contains("--child"))
        {
            return RunChild();
        }

        string? outputDirectory = ValueAfter(args, "--output-dir");
        bool selfTest = args.Contains("--self-test");
        if (outputDirectory is null)
        {
            Console.Error.WriteLine("--output-dir is required");
            return 64;
        }

        try
        {
            return RunHost(Path.GetFullPath(outputDirectory), selfTest).GetAwaiter().GetResult();
        }
        catch (Exception exception)
        {
            Console.Error.WriteLine(exception);
            return 1;
        }
    }

    private static string? ValueAfter(string[] args, string name)
    {
        int index = Array.IndexOf(args, name);
        return index >= 0 && index + 1 < args.Length ? args[index + 1] : null;
    }

    private static int RunChild()
    {
        IntPtr input = GetStdHandle(StdInputHandle);
        IntPtr output = GetStdHandle(StdOutputHandle);

        if (!GetConsoleMode(input, out uint inputMode))
        {
            Console.Error.WriteLine($"GetConsoleMode(stdin) failed: {Marshal.GetLastWin32Error()}");
            return 2;
        }

        inputMode |= EnableProcessedInput | EnableLineInput | EnableEchoInput;
        if (!SetConsoleMode(input, inputMode))
        {
            Console.Error.WriteLine($"SetConsoleMode(stdin) failed: {Marshal.GetLastWin32Error()}");
            return 3;
        }

        if (GetConsoleMode(output, out uint outputMode))
        {
            SetConsoleMode(output, outputMode | EnableProcessedOutput | EnableVirtualTerminalProcessing);
        }

        Console.OutputEncoding = new UTF8Encoding(false);
        Console.WriteLine("WINDOWS CONPTY NATIVE LINE-EDIT TRIAL");
        Console.WriteLine("Type a draft without pressing Enter.");
        Console.WriteLine("For physical Del: press Home, then Del once per character.");
        Console.WriteLine("Type a different final sentence, then press Enter once.");
        Console.WriteLine();
        Console.Out.Flush();

        var buffer = new StringBuilder(4096);
        if (!ReadConsoleW(input, buffer, 4095, out uint charactersRead, IntPtr.Zero))
        {
            Console.Error.WriteLine($"ReadConsoleW failed: {Marshal.GetLastWin32Error()}");
            return 4;
        }

        string committed = buffer.ToString(0, checked((int)charactersRead)).TrimEnd('\r', '\n');
        Console.WriteLine($"CHILD_RECEIVED: {committed}");
        Console.Out.Flush();
        return 0;
    }

    private static async Task<int> RunHost(string outputDirectory, bool selfTest)
    {
        Directory.CreateDirectory(outputDirectory);
        (string transcriptPath, string metadataPath) = ChoosePaths(outputDirectory, selfTest);

        EnableParentVirtualTerminalOutput();

        using var inputPipe = new PseudoConsolePipe();
        using var outputPipe = new PseudoConsolePipe();
        using var pseudoConsole = PseudoConsole.Create(
            inputPipe.ReadSide,
            outputPipe.WriteSide,
            width: Math.Max(80, Console.WindowWidth),
            height: Math.Max(25, Console.WindowHeight));

        string executable = Environment.ProcessPath
            ?? throw new InvalidOperationException("Could not resolve the current executable path.");
        string commandLine = $"\"{executable}\" --child";
        using var child = ChildProcess.Start(commandLine, pseudoConsole.Handle);

        Task outputTask = CopyOutputAsync(outputPipe.ReadSide, transcriptPath);

        int homeKeyCount = 0;
        int deleteKeyCount = 0;
        int backspaceKeyCount = 0;

        using (var inputStream = new FileStream(inputPipe.WriteSide, FileAccess.Write, 4096, isAsync: false))
        {
            if (selfTest)
            {
                await Task.Delay(250);
                WriteUtf8(inputStream, "alpha");
                WriteUtf8(inputStream, "\x1b[H");
                for (int i = 0; i < 5; i++)
                {
                    WriteUtf8(inputStream, "\x1b[3~");
                }
                WriteUtf8(inputStream, "omega\r");
            }
            else
            {
                while (true)
                {
                    ConsoleKeyInfo key = Console.ReadKey(intercept: true);
                    string sequence = KeyToSequence(key);
                    if (sequence.Length == 0)
                    {
                        continue;
                    }

                    if (key.Key == ConsoleKey.Home) homeKeyCount++;
                    if (key.Key == ConsoleKey.Delete) deleteKeyCount++;
                    if (key.Key == ConsoleKey.Backspace) backspaceKeyCount++;

                    WriteUtf8(inputStream, sequence);
                    if (key.Key == ConsoleKey.Enter)
                    {
                        break;
                    }
                }
            }
        }

        bool exited = child.WaitForExit(TimeSpan.FromSeconds(15));
        int childExitCode = exited ? child.ExitCode : -1;

        pseudoConsole.Close();
        outputPipe.WriteSide.Dispose();
        await outputTask.WaitAsync(TimeSpan.FromSeconds(10));

        byte[] transcript = await File.ReadAllBytesAsync(transcriptPath);
        string transcriptText = Encoding.UTF8.GetString(transcript);
        bool selfTestPassed = !selfTest ||
            (transcriptText.Contains("alpha", StringComparison.Ordinal) &&
             transcriptText.Contains("CHILD_RECEIVED: omega", StringComparison.Ordinal) &&
             !transcriptText.Contains("CHILD_RECEIVED: alpha", StringComparison.Ordinal));

        var metadata = new
        {
            method = "native-windows-conpty-line-edit-v1",
            status = exited && childExitCode == 0 && selfTestPassed ? "success" : "failure",
            input_source = selfTest ? "scripted-self-test" : "physical-console-keys",
            transcript_path = Path.GetFullPath(transcriptPath),
            transcript_bytes = transcript.Length,
            transcript_sha256 = Convert.ToHexString(SHA256.HashData(transcript)).ToLowerInvariant(),
            home_key_count = homeKeyCount,
            delete_key_count = deleteKeyCount,
            backspace_key_count = backspaceKeyCount,
            child_exit_code = childExitCode,
            self_test_passed = selfTest ? selfTestPassed : null as bool?,
            operating_system = RuntimeInformation.OSDescription,
            framework = RuntimeInformation.FrameworkDescription,
            architecture = RuntimeInformation.ProcessArchitecture.ToString()
        };
        await File.WriteAllTextAsync(
            metadataPath,
            JsonSerializer.Serialize(metadata, new JsonSerializerOptions { WriteIndented = true }) + Environment.NewLine);

        Console.WriteLine();
        Console.WriteLine($"STATUS={metadata.status}");
        Console.WriteLine($"TRANSCRIPT_PATH={metadata.transcript_path}");
        Console.WriteLine($"METADATA_PATH={Path.GetFullPath(metadataPath)}");
        Console.WriteLine($"TRANSCRIPT_SHA256={metadata.transcript_sha256}");
        return metadata.status == "success" ? 0 : 5;
    }

    private static string KeyToSequence(ConsoleKeyInfo key)
    {
        return key.Key switch
        {
            ConsoleKey.Enter => "\r",
            ConsoleKey.Backspace => "\x7f",
            ConsoleKey.Delete => "\x1b[3~",
            ConsoleKey.Home => "\x1b[H",
            ConsoleKey.End => "\x1b[F",
            ConsoleKey.LeftArrow => "\x1b[D",
            ConsoleKey.RightArrow => "\x1b[C",
            ConsoleKey.UpArrow => "\x1b[A",
            ConsoleKey.DownArrow => "\x1b[B",
            ConsoleKey.Escape => "\x1b",
            _ when key.Modifiers.HasFlag(ConsoleModifiers.Control) && key.Key == ConsoleKey.C => "\x03",
            _ when key.KeyChar != '\0' => key.KeyChar.ToString(),
            _ => ""
        };
    }

    private static void WriteUtf8(Stream stream, string value)
    {
        byte[] bytes = Encoding.UTF8.GetBytes(value);
        stream.Write(bytes, 0, bytes.Length);
        stream.Flush();
    }

    private static async Task CopyOutputAsync(SafeFileHandle outputReadSide, string transcriptPath)
    {
        await using var pseudoConsoleOutput = new FileStream(outputReadSide, FileAccess.Read, 4096, isAsync: false);
        await using var transcript = new FileStream(
            transcriptPath, FileMode.CreateNew, FileAccess.Write, FileShare.Read, 4096, useAsync: true);
        await using Stream terminalOutput = Console.OpenStandardOutput();
        byte[] buffer = new byte[4096];
        while (true)
        {
            int count = await pseudoConsoleOutput.ReadAsync(buffer);
            if (count == 0)
            {
                break;
            }
            await terminalOutput.WriteAsync(buffer.AsMemory(0, count));
            await terminalOutput.FlushAsync();
            await transcript.WriteAsync(buffer.AsMemory(0, count));
            await transcript.FlushAsync();
        }
    }

    private static void EnableParentVirtualTerminalOutput()
    {
        IntPtr output = GetStdHandle(StdOutputHandle);
        if (GetConsoleMode(output, out uint mode))
        {
            SetConsoleMode(output, mode | EnableProcessedOutput | EnableVirtualTerminalProcessing | DisableNewlineAutoReturn);
        }
    }

    private static (string Transcript, string Metadata) ChoosePaths(string directory, bool selfTest)
    {
        string label = selfTest ? "conpty-self-test" : "conpty-experiment";
        string stamp = DateTime.Now.ToString("yyyyMMdd-HHmmss");
        string stem = Path.Combine(directory, $"{label}-{stamp}");
        int suffix = 2;
        string transcript = stem + ".typescript";
        string metadata = stem + ".metadata.json";
        while (File.Exists(transcript) || File.Exists(metadata))
        {
            transcript = stem + $"-{suffix}.typescript";
            metadata = stem + $"-{suffix}.metadata.json";
            suffix++;
        }
        return (transcript, metadata);
    }

    private sealed class PseudoConsolePipe : IDisposable
    {
        public SafeFileHandle ReadSide { get; }
        public SafeFileHandle WriteSide { get; }

        public PseudoConsolePipe()
        {
            if (!CreatePipe(out SafeFileHandle readSide, out SafeFileHandle writeSide, IntPtr.Zero, 0))
            {
                throw new InvalidOperationException($"CreatePipe failed: {Marshal.GetLastWin32Error()}");
            }
            ReadSide = readSide;
            WriteSide = writeSide;
        }

        public void Dispose()
        {
            ReadSide.Dispose();
            WriteSide.Dispose();
        }
    }

    private sealed class PseudoConsole : IDisposable
    {
        public IntPtr Handle { get; private set; }

        private PseudoConsole(IntPtr handle) => Handle = handle;

        public static PseudoConsole Create(
            SafeFileHandle inputReadSide,
            SafeFileHandle outputWriteSide,
            int width,
            int height)
        {
            int result = CreatePseudoConsole(
                new Coord { X = (short)width, Y = (short)height },
                inputReadSide,
                outputWriteSide,
                0,
                out IntPtr handle);
            if (result != 0)
            {
                throw new InvalidOperationException($"CreatePseudoConsole failed with HRESULT 0x{result:x8}");
            }
            return new PseudoConsole(handle);
        }

        public void Close()
        {
            if (Handle != IntPtr.Zero)
            {
                ClosePseudoConsole(Handle);
                Handle = IntPtr.Zero;
            }
        }

        public void Dispose() => Close();
    }

    private sealed class ChildProcess : IDisposable
    {
        private StartupInfoEx _startupInfo;
        private ProcessInformation _processInfo;

        private ChildProcess(StartupInfoEx startupInfo, ProcessInformation processInfo)
        {
            _startupInfo = startupInfo;
            _processInfo = processInfo;
        }

        public static ChildProcess Start(string commandLine, IntPtr pseudoConsole)
        {
            IntPtr size = IntPtr.Zero;
            InitializeProcThreadAttributeList(IntPtr.Zero, 1, 0, ref size);
            if (size == IntPtr.Zero)
            {
                throw new InvalidOperationException("Could not size the process attribute list.");
            }

            var startupInfo = new StartupInfoEx
            {
                StartupInfo = new StartupInfo { Cb = Marshal.SizeOf<StartupInfoEx>() },
                AttributeList = Marshal.AllocHGlobal(size)
            };

            if (!InitializeProcThreadAttributeList(startupInfo.AttributeList, 1, 0, ref size))
            {
                throw new InvalidOperationException($"InitializeProcThreadAttributeList failed: {Marshal.GetLastWin32Error()}");
            }
            if (!UpdateProcThreadAttribute(
                    startupInfo.AttributeList,
                    0,
                    (IntPtr)ProcThreadAttributePseudoConsole,
                    pseudoConsole,
                    (IntPtr)IntPtr.Size,
                    IntPtr.Zero,
                    IntPtr.Zero))
            {
                throw new InvalidOperationException($"UpdateProcThreadAttribute failed: {Marshal.GetLastWin32Error()}");
            }

            var processSecurity = new SecurityAttributes { Length = Marshal.SizeOf<SecurityAttributes>() };
            var threadSecurity = new SecurityAttributes { Length = Marshal.SizeOf<SecurityAttributes>() };
            var mutableCommandLine = new StringBuilder(commandLine);
            if (!CreateProcessW(
                    null,
                    mutableCommandLine,
                    ref processSecurity,
                    ref threadSecurity,
                    false,
                    ExtendedStartupInfoPresent,
                    IntPtr.Zero,
                    null,
                    ref startupInfo,
                    out ProcessInformation processInfo))
            {
                throw new InvalidOperationException($"CreateProcessW failed: {Marshal.GetLastWin32Error()}");
            }
            return new ChildProcess(startupInfo, processInfo);
        }

        public bool WaitForExit(TimeSpan timeout)
        {
            uint milliseconds = timeout == Timeout.InfiniteTimeSpan
                ? 0xffffffff
                : checked((uint)timeout.TotalMilliseconds);
            return WaitForSingleObject(_processInfo.Process, milliseconds) == 0;
        }

        public int ExitCode
        {
            get
            {
                if (!GetExitCodeProcess(_processInfo.Process, out uint code))
                {
                    throw new InvalidOperationException($"GetExitCodeProcess failed: {Marshal.GetLastWin32Error()}");
                }
                return unchecked((int)code);
            }
        }

        public void Dispose()
        {
            if (_startupInfo.AttributeList != IntPtr.Zero)
            {
                DeleteProcThreadAttributeList(_startupInfo.AttributeList);
                Marshal.FreeHGlobal(_startupInfo.AttributeList);
                _startupInfo.AttributeList = IntPtr.Zero;
            }
            if (_processInfo.Process != IntPtr.Zero) CloseHandle(_processInfo.Process);
            if (_processInfo.Thread != IntPtr.Zero) CloseHandle(_processInfo.Thread);
        }
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct Coord { public short X; public short Y; }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    private struct StartupInfoEx
    {
        public StartupInfo StartupInfo;
        public IntPtr AttributeList;
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    private struct StartupInfo
    {
        public int Cb;
        public IntPtr Reserved;
        public IntPtr Desktop;
        public IntPtr Title;
        public int X;
        public int Y;
        public int XSize;
        public int YSize;
        public int XCountChars;
        public int YCountChars;
        public int FillAttribute;
        public int Flags;
        public short ShowWindow;
        public short Reserved2;
        public IntPtr ReservedPointer;
        public IntPtr StdInput;
        public IntPtr StdOutput;
        public IntPtr StdError;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct ProcessInformation
    {
        public IntPtr Process;
        public IntPtr Thread;
        public int ProcessId;
        public int ThreadId;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct SecurityAttributes
    {
        public int Length;
        public IntPtr SecurityDescriptor;
        public int InheritHandle;
    }

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool CreatePipe(
        out SafeFileHandle readPipe,
        out SafeFileHandle writePipe,
        IntPtr pipeAttributes,
        int size);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern int CreatePseudoConsole(
        Coord size,
        SafeFileHandle input,
        SafeFileHandle output,
        uint flags,
        out IntPtr pseudoConsole);

    [DllImport("kernel32.dll")]
    private static extern void ClosePseudoConsole(IntPtr pseudoConsole);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool InitializeProcThreadAttributeList(
        IntPtr attributeList,
        int attributeCount,
        int flags,
        ref IntPtr size);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool UpdateProcThreadAttribute(
        IntPtr attributeList,
        uint flags,
        IntPtr attribute,
        IntPtr value,
        IntPtr size,
        IntPtr previousValue,
        IntPtr returnSize);

    [DllImport("kernel32.dll")]
    private static extern void DeleteProcThreadAttributeList(IntPtr attributeList);

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern bool CreateProcessW(
        string? applicationName,
        StringBuilder commandLine,
        ref SecurityAttributes processAttributes,
        ref SecurityAttributes threadAttributes,
        bool inheritHandles,
        uint creationFlags,
        IntPtr environment,
        string? currentDirectory,
        ref StartupInfoEx startupInfo,
        out ProcessInformation processInformation);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern uint WaitForSingleObject(IntPtr handle, uint milliseconds);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool GetExitCodeProcess(IntPtr process, out uint exitCode);

    [DllImport("kernel32.dll")]
    private static extern bool CloseHandle(IntPtr handle);

    [DllImport("kernel32.dll")]
    private static extern IntPtr GetStdHandle(int standardHandle);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool GetConsoleMode(IntPtr consoleHandle, out uint mode);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool SetConsoleMode(IntPtr consoleHandle, uint mode);

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern bool ReadConsoleW(
        IntPtr consoleInput,
        [Out] StringBuilder buffer,
        uint charactersToRead,
        out uint charactersRead,
        IntPtr inputControl);
}
