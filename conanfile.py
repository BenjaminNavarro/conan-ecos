from conans import ConanFile, CMake, tools


class EcosConan(ConanFile):
    name = "ecos"
    version = "2.0.7"
    license = "MIT"
    author = "Benjamin Navarro <navarro.benjamin13@gmail.com>"
    url = "https://github.com/BenjaminNavarro/conan-ecos"
    description = "Conan package for the ECOS library, a lightweight conic solver for second-order cone programming"
    topics = ("C++", "SOCP", "Solver")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    _libs = ["ecos"]

    def source(self):
        git = tools.Git(folder="ecos")
        git.clone("https://github.com/embotech/ecos.git")
        git.checkout("3d2f48bf788cf8445ea0c38fe767a10d4166e708")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="ecos")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include/ecos", src="ecos/include")
        self.copy("*.h", dst="include/SuiteSparse_config", src="ecos/external/SuiteSparse_config")
        self.copy("COPYING", src="ecos")

        for lib in self._libs:
            self.copy("*{}.lib".format(lib), dst="lib", keep_path=False)
            self.copy("*{}.dll".format(lib), dst="bin", keep_path=False)
            self.copy("*{}.so".format(lib), dst="lib", keep_path=False)
            self.copy("*{}.dylib".format(lib), dst="lib", keep_path=False)
            self.copy("*{}.a".format(lib), dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = self._libs
        self.cpp_info.includedirs = ["include/ecos", "include/SuiteSparse_config"]
        self.cpp_info.defines = ["CTRLC=1", "LDL_LONG", "DLONG"]
