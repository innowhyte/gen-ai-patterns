.PHONY: unescape-md-parens

unescape-md-parens:
	@if command -v rg >/dev/null 2>&1; then \
		rg --files -g '*.md' | xargs perl -pi -e 's/\\\(/(/g; s/\\\)/)/g'; \
	else \
		find . -type f -name '*.md' -print0 | xargs -0 perl -pi -e 's/\\\(/(/g; s/\\\)/)/g'; \
	fi
