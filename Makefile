RELEASE_BRANCH := html
RELEASE_REPO := https://github.com/aleksey925/knowledge-base.git
OUTPUT ?= dist

build:
	rm -rf $(OUTPUT)
	scrawl site -o $(OUTPUT) src

b: build

publish: build
	cd $(OUTPUT) \
	&& git init \
	&& git config --local user.name "ci user" \
	&& git config --local user.email "ci@ci.com" \
	&& git add . \
	&& git commit -m 'init' \
	&& git remote add origin ${RELEASE_REPO} \
	&& git branch -m ${RELEASE_BRANCH} \
	&& git push -u origin ${RELEASE_BRANCH} -f
