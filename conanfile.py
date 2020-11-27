from conans import ConanFile, CMake, tools
import os


class GlbindingConan(ConanFile):
    name = "glbinding"
    description = "Create and optimize SPIRV shaders"
    license = "Apache-2.0"
    topics = ("conan", "spirv-tools", "spirv", "spirv-v", "vulkan", "opengl", "opencl", "hlsl", "khronos")
    homepage = "https://github.com/KhronosGroup/SPIRV-Tools"
    url = "https://github.com/conan-io/conan-center-index"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports_sources = ["CMakeLists.txt", "patches/**"]
    generators = "cmake"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename(self.name + "-" + self.version, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["OPTION_SELF_CONTAINED"] = False
        self._cmake.definitions["OPTION_BUILD_TESTS"] = False
        self._cmake.definitions["OPTION_BUILD_DOCS"] = False
        self._cmake.definitions["OPTION_BUILD_TOOLS"] = False
        self._cmake.definitions["OPTION_BUILD_EXAMPLES"] = False
        self._cmake.definitions["OPTION_BUILD_WITH_BOOST_THREAD"] = False
        self._cmake.definitions["OPTION_BUILD_CHECK"] = False
        self._cmake.configure()
        return self._cmake

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()
        tools.rmdir(os.path.join(self.package_folder, "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "glbinding"
        self.cpp_info.names["cmake_find_package_multi"] = "glbinding"
        # glbinding
        self.cpp_info.components["_glbinding"].names["cmake_find_package"] = "glbinding"
        self.cpp_info.components["_glbinding"].names["cmake_find_package_multi"] = "glbinding"
        self.cpp_info.components["_glbinding"].libs = ["glbinding"]
        self.cpp_info.components["_glbinding"].requires = ["khrplatform"]
        # glbinding-aux
        self.cpp_info.components["glbinding-aux"].names["cmake_find_package"] = "glbinding-aux"
        self.cpp_info.components["glbinding-aux"].names["cmake_find_package_multi"] = "glbinding-aux"
        self.cpp_info.components["glbinding-aux"].libs = ["glbinding-aux"]
        self.cpp_info.components["glbinding-aux"].requires = ["_glbinding"]
        # KHRplatform
        self.cpp_info.components["khrplatform"].names["cmake_find_package"] = "KHRplatform"
        self.cpp_info.components["khrplatform"].names["cmake_find_package_multi"] = "KHRplatform"
        self.cpp_info.components["glbinding-aux"].libdirs = []
