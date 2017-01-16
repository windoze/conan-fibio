from conans import ConanFile, CMake, tools
import os


class FibioConan(ConanFile):
    name = "fibio"
    version = "0.6"
    license = "Simplified BSD License - https://opensource.org/licenses/BSD-2-Clause"
    url = "https://github.com/windoze/fibio"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    description = "Fiberized IO"

    def configure(self):
        self.requires("Boost/1.63.0@windoze/stable")
        self.options["Boost/1.63.0"].shared = self.options.shared                    

    def source(self):
        self.run("git clone https://github.com/windoze/fibio.git")
        self.run("cd fibio && git checkout conan")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("fibio/CMakeLists.txt", "PROJECT(fibio)", '''PROJECT(fibio)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
        self.run('cmake fibio %s %s' % (cmake.command_line, shared))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("asio.hpp", dst="include/fibio", src="fibio/include/fibio")
        self.copy("*.hpp", dst="include/fibio/concurrent", src="fibio/include/fibio/concurrent")
        self.copy("fiber.hpp", dst="include/fibio", src="fibio/include/fibio")
        self.copy("fiberize.hpp", dst="include/fibio", src="fibio/include/fibio")
        self.copy("*.hpp", dst="include/fibio/fibers", src="fibio/include/fibio/fibers")
        self.copy("*.hpp", dst="include/fibio/fibers/asio", src="fibio/include/fibio/fibers/asio")
        self.copy("*.hpp", dst="include/fibio/fibers/asio/detail", src="fibio/include/fibio/fibers/asio/detail")
        self.copy("*.hpp", dst="include/fibio/fibers/detail", src="fibio/include/fibio/fibers/detail")
        self.copy("*.hpp", dst="include/fibio/fibers/future", src="fibio/include/fibio/fibers/future")
        self.copy("*.hpp", dst="include/fibio/fibers/future/detail", src="fibio/include/fibio/fibers/future/detail")
        self.copy("future.hpp", dst="include/fibio", src="fibio/include/fibio")
        self.copy("iostream.hpp", dst="include/fibio", src="fibio/include/fibio")
        self.copy("*.hpp", dst="include/fibio/stream", src="fibio/include/fibio/stream")
        self.copy("thrift.hpp", dst="include/fibio", src="fibio/include/fibio")
        self.copy("utility.hpp", dst="include/fibio", src="fibio/include/fibio")
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.dll", dst="bin", src="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", src="src", keep_path=False)
        self.copy("*.so", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["fibio"]
