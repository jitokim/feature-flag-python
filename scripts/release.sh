#!/usr/bin/env bash
set -euo pipefail

# Usage: make release VERSION=1.2.3

VERSION=${VERSION:-""}

if [[ -z "$VERSION" ]]; then
  echo "❌ VERSION 환경변수를 지정해주세요. 예: make release VERSION=1.2.3"
  exit 1
fi

echo "📦 릴리즈 버전: v$VERSION"

# 1. Git 태그 생성
git tag -a "v$VERSION" -m "Release v$VERSION"

# 2. GitHub에 태그 푸시
git push origin "v$VERSION"

echo "🚀 태그가 푸시되었습니다. GitHub Actions에서 자동으로 배포됩니다!"
