# ScyllaDB Documentation Style Guide

## Table of Contents
- [Introduction](#introduction)
- [Highlights (Quick Rules)](#highlights-quick-rules)
- [Word Choice](#word-choice)
- [Language and Grammar](#language-and-grammar)
- [Formatting](#formatting)
- [Page Titles](#page-titles)
- [Lists](#lists)
- [URLs and File Names](#urls-and-file-names)
- [Labels](#labels)
- [Diagrams](#diagrams)
- [Admonitions](#admonitions)
- [Static Documentation](#static-documentation)
- [Audience](#audience)
- [Accessible Writing](#accessible-writing)

## Introduction
This guide defines the standard style all ScyllaDB content to keep everything consistent.

---

## Highlights (Quick Rules)

- Use **second person ("you")**
  - ✅ You will be redirected to the login page.
  - ❌ The user will be redirected to the login page.

- Use **active voice**
  - ✅ ScyllaDB supports the following versions:
  - ❌ The following versions are supported by Scylla.

- Use **numbered lists** for sequences:
  1. Provide your credentials.
  2. Click OK.
  3. Refresh the page.

- Use **bulleted lists** when order doesn’t matter:
  - Change the log file name.
  - Copy the log file.
  - Remove the log file.

- **Bold UI elements**
  - ✅ Click **Options**.
  - ❌ Click “Options”.

- **Avoid pre-announcements**
  - ❌ We will add a workaround soon.
  - ❌ This option will be supported in the next release.

- **Punctuation**
  - Capitalize sentence starts.
  - End sentences with a period.
  - Use a colon before lists.

- **Tone**
  - Be conversational and clear.
  - Prefer short, direct sentences.

- **Spelling**
  - Use American English.

---

## Word Choice

### Preferred Terms

- ScyllaDB (not Scylla)
- keyspace (not key space)
- SSTable (not Sstable, ssTable)
- click (not press, for UI)
- select (not check, mark)
- datacenter (not data center)
- multicloud (not multi-cloud)
- codebase (not code base)
- multi-datacenter (not multi DC variants)
- vnode (not Vnode)

---

## Language and Grammar

### Active Voice
Use active voice whenever possible.

- ❌ When the window is closed, the transfer will begin.
- ✅ When you close the window, the transfer will begin.

### Addressing the User
- ❌ The user must enter credentials.
- ✅ Enter your credentials.

### Tone
- Be friendly, natural, and concise.
- Use contractions when appropriate.
- Prefer clarity over formality.

**Example:**
- ❌ If you want to install ScyllaDB, go to the download center.
- ✅ Install ScyllaDB from the download center.

### Pronouns
Avoid ambiguity.

- ❌ If you type text in the field, it doesn't change. (Not clear if “it” “refers to “text” or “field”).
- ✅ If you type text in the field, the text doesn't change.

### Spelling
- Use standard American spelling (e.g., *analyze*, not *analyse*).

### Comma (Oxford Comma)
- ✅ consistency, availability, and partition tolerance
- ❌ consistency, availability and partition tolerance

---

## Formatting

### UI Elements
Bold all UI elements:
- Click **Create Policy**.

### Key Terms
Use *italics* when introducing new concepts:
- A *node* is a unit of storage.

### Code Samples
- Do not prefix commands with `$`
- Separate command and output blocks
- Do not include real customer data

### Command Reference Format
Use this structure:
- Name
- Description
- Syntax
- Parameters
- Example

---

## Page Titles
- Keep titles under ~60 characters
- Avoid truncation in search results

---

## Lists

### Numbered (Ordered)
Use when sequence matters:
1. Stop service 1.
2. Stop service 2.
3. Start service 3.

### Bulleted (Unordered)
Use when order doesn’t matter:
- Windows 10
- Docker Desktop
- Java 8

---

## URLs and File Names
- Use short, descriptive names
- Use hyphens (`-`), not underscores (`_`)

---

## Admonitions

Use sparingly:

- ``.. note::``: Additional helpful info
- ``.. tip:``: Improves performance or workflow
- ``.. caution:``: Risk of performance issues
- ``.. warning:``: Risk of data loss, crashes, or harm

---

## Labels

### Available Labels

- ``:label-default:``
- ``:label-note:``
- ``:label-tip:``
- ``:label-caution:``
- ``:label-warning:``


### Usage Examples
-  ``:label-caution:``Experimental
- ``:label-tip:``Available with the Professional plan and above

---

## Diagrams
- Minimize text inside diagrams
- Use labels + legend tables instead
- Architecture diagrams should show **8 nodes per cluster**

---

## Static Documentation
- Avoid temporary statements
- Do not pre-announce features

**Exceptions:**
- Compatibility notes (e.g., Cassandra differences, Alternator)

---

## Audience
Primary audience:
- Developers
- Database administrators

Do not assume:
- NoSQL experience
- Cassandra familiarity
- AWS usage
- Single-node setups

Also consider:
- Non-technical readers (e.g., executives)

---

## Accessible Writing
Ensure documentation is accessible:

- Add alt text to images
- Support screen readers
- Avoid poor color contrast
- Keep diagrams simple

---
