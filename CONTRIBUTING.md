# Contributing to LangGraph

Thank you for being interested in contributing to LangGraph!

## General guidelines

Here are some things to keep in mind for all types of contributions:

- Follow the ["fork and pull request"](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project) workflow.
- Fill out the checked-in pull request template when opening pull requests. Note related issues and tag relevant maintainers.
- Ensure your PR passes formatting, linting, and testing checks before requesting a review.
  - If you would like comments or feedback, please open an issue or discussion and tag a maintainer.
- Backwards compatibility is key. Your changes must not be breaking, except in case of critical bug and security fixes.
- Look for duplicate PRs or issues that have already been opened before opening a new one.
- Keep scope as isolated as possible. As a general rule, your changes should not affect more than one package at a time.

### Bugfixes

For bug fixes, please open up an issue before proposing a fix to ensure the proposal properly addresses the underlying problem. In general, bug fixes should all have an accompanying unit test that fails before the fix.

### New features

For new features, please start a new [discussion](https://github.com/langchain-ai/langgraph/discussions), where the maintainers will help with scoping out the necessary changes.

## Contribute Documentation

Documentation is a vital part of LangGraph. We welcome both new documentation for new features and
community improvements to our current documentation. Please read the resources below before getting started:

- [Documentation style guide](#documentation-style-guide)
- [Documentation setup](#setup)

## Documentation Style Guide

As LangGraph continues to grow, the surface area of documentation required to cover it continues to grow too.
This page provides guidelines for anyone writing documentation for LangGraph, as well as some of our philosophies around organization and structure.

### How-to guides

A how-to guide, as the name implies, demonstrates how to do something discrete and specific.
It should assume that the user is already familiar with underlying concepts, and is trying to solve an immediate problem, but
should still give some background or list the scenarios where the information contained within can be relevant.
They can and should discuss alternatives if one approach may be better than another in certain cases.