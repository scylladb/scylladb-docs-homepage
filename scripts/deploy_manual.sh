#!/usr/bin/env bash

# Variables
REPO_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
GH_PAGES_DIR="gh-pages"

echo "Preparing docs dir..."
mkdir -p $GH_PAGES_DIR
cp -r ./submodules/scylladb/docs/_build/dirhtml/. $GH_PAGES_DIR

if git ls-remote --heads "$REPO_URL" gh-pages; then
    echo "Cloning existing gh-pages branch..."
    git clone --branch gh-pages --single-branch "$REPO_URL" "${GH_PAGES_DIR}-existing"
    cd "${GH_PAGES_DIR}-existing"

    echo "Cleaning up existing content..."
    rm -rf manual

    echo "Copying new documentation..."
    mkdir -p manual
    cp -a ../$GH_PAGES_DIR/. manual/

    echo "Configuring Git..."
    git config --local user.email "action@scylladb.com"
    git config --local user.name "GitHub Action"

    echo "Committing and pushing changes..."
    git add .
    git commit -m "Update docs" || true
    git push origin gh-pages --force

else
    echo "Error: The gh-pages branch does not exist in the repository."
    echo "Please create a gh-pages branch in your repository and re-run the script."
    exit 1
fi
