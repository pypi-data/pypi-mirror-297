import setuptools


def _make_long_description():
	with open("README.md", "r", encoding="utf-8") as readme_file:
		readme_content = readme_file.read()

	fr_index = readme_content.index("## FRANÇAIS")
	fr_demos_index = readme_content.index("### Démo")
	en_index = readme_content.index("## ENGLISH")
	en_demos_index = readme_content.index("### Demo")

	return readme_content[fr_index:fr_demos_index]\
		+ readme_content[en_index:en_demos_index].rstrip()


if __name__ == "__main__":
	setuptools.setup(
		name = "syspathmodif",
		version = "0.0.2",
		author = "Guyllaume Rousseau",
		description = "This library offers concise manners to modify list sys.path. The user should not need to import module sys.",
		long_description = _make_long_description(),
		long_description_content_type = "text/markdown",
		url = "https://github.com/GRV96/syspathmodif",
		classifiers = [
			"Development Status :: 5 - Production/Stable",
			"Intended Audience :: Developers",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			"Programming Language :: Python :: 3",
			"Topic :: Software Development :: Libraries :: Python Modules",
			"Topic :: Utilities"
		],
		packages = setuptools.find_packages(exclude=(".github", "demo", "demo_package",)),
		license = "MIT",
		license_files = ("LICENSE",))
