import setuptools


def _make_long_description():
	with open("README.md", "r", encoding="utf-8") as readme_file:
		readme_content = readme_file.read()

	fr_index = readme_content.index("## FRANÇAIS")
	fr_dependencies_index = readme_content.index("### Dépendances")
	en_index = readme_content.index("## ENGLISH")
	en_dependencies_index = readme_content.index("### Dependencies")

	return readme_content[fr_index:fr_dependencies_index]\
		+ readme_content[en_index:en_dependencies_index].rstrip()


def _make_requirement_list():
	with open("requirements.txt", "r", encoding="utf-8") as req_file:
		req_str = req_file.read()

	raw_requirements = req_str.split("\n")

	requirements = list()
	for requirement in raw_requirements:
		if len(requirement) > 0:
			requirements.append(requirement)

	return requirements


if __name__ == "__main__":
	setuptools.setup(
		name = "repr_rw",
		version = "1.0.2",
		author = "Guyllaume Rousseau",
		description = "This library writes Python object representations in a text file and reads the file to recreate the objects. An object representation is a string returned by function repr.",
		long_description = _make_long_description(),
		long_description_content_type = "text/markdown",
		url = "https://github.com/GRV96/repr_rw",
		classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
		install_requires = _make_requirement_list(),
		packages = setuptools.find_packages(exclude=("demos", "demo_package",)),
		license = "MIT",
		license_files = ("LICENSE",))
