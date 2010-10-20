import subprocess
import os.path


class Compile:
    def __init__(self, config):
        self.config = config

    def compile_source(self, source_filepath, lang=None):
        compiler = self.get_compiler(source_filepath, lang)
        compiler.get_compile_cmd(source_filepath)
        print compile_cmd
        child = subprocess.Popen(compile_cmd, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
        out, err = child.communicate()
        retDict = {}
        retDict["retcode"] = child.returncode
        retDict["compiler_output"] = out + err
        retDict["run_cmd"] = compiler.get_run_cmd(source_filepath)
        return retDict

    # determines the language from the extension or from the lang
    # argument if one is supplied.
    def get_compiler(self, source_filepath, lang=None):
        if lang == None:
            # TODO: determine language from source_file and set it in
            # lang
            pass
        if lang == "C":
            return C_Compiler(self.config)
        elif lang == "CPP":
            return CPP_Compiler(self.config)
        elif lang == "PY":
            return Py_Compiler(self.config)
        elif lang == "JAVA":
            return Java_Compiler(self.config)


class C_Compile:
    """
    This is a language specific compiler class. It needs all the
    methods needed below below.
    """
    def __init__(self, config):
        self.config = config
        self.compile_cmd = config.config.get("CompileCommands", "C_compile")
        self.exec_string = config.config.get("CompileCommands", "C_run")

    def get_compile_cmd(self, source_path):
        basename = os.path.join(self.config.abs_path, str(submission.pk))
        return self.compile_cmd.replace("%s", basename + ".c").replace("%e", \
            basename + ".exe")

    def get_run_cmd(self, source_path):
        basename = os.path.join(self.config.abs_path, str(submission.ph))
        return self.exec_string.replace("%e", basename + ".exe")
