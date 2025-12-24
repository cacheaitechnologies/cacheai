# Cache AI Naming Guide

**Engineering Naming & Documentation Convention**

## Purpose

This document establishes **consistent naming and notation rules** in the **Cache AI repository** for:

* Technical documentation
* Implementation code
* Diagrams and specifications

The goal is to help engineers choose the correct notation based on context without confusion.

---

## Summary

* **Cache AI**: Registered trademark, product name, technology name, concept
* **Cache AI API**: API providing the concept
* **CacheAI ○○**: Technology/product/service/organization proper nouns (combinations)
* **`cacheai` family**: Code identifiers

---

## Notation Categories and Rules

### 1. Core Technology/Product/Service Name


**Notation**

* **Cache AI** (with space)

**Usage Examples**

* Cache AI is a semantic caching layer for LLM inference.
* Cache AI reduces redundant LLM computation.
* This document explains the core concept of Cache AI.

**Rationale**

* **Cache AI** (with space) is a **registered trademark and product name**.
* Legal and trademark-compliant official designation
* Can be used as technology/product/service name or concept


**Important Notes**

* In conceptual contexts, use **Cache AI**, do **not** write **CacheAI**
* Do not confuse with other product names or organization names

---

### 2. Identifier

**Definition**
Names that **machines interpret**, such as code, configuration, and API paths.

**Notation**

* `cacheai`
* `CACHEAI`
* `CacheAI`
* `cacheAI`

※ Choose based on purpose, language, and conventions

**Usage Examples**

```python
import cacheai

CACHEAI_TIMEOUT=30

class CacheAIClient:
```

**Applicable Scope**

* Package names
* Class names
* Environment variables
* API paths
* HTTP headers
* CLI commands

---

### 3. Other Technology/Product/Service/Organization Names (Proper Noun)

**Definition**
Proper nouns for **technology/product/service/organization names** related to CacheAI Technologies.

**Notation Rule**

> **CacheAI + Technology/Product/Service/Organization Name**

**Usage Examples**

* CacheAI Enterprise
* CacheAI Console

**Rationale**

* Consistent with company name (CacheAI Technologies)
* Complies with legal documentation

---

## API Notation Rules

### API (as a Concept)

**Notation**

* **Cache AI API**

**Meaning**

* API that provides the Cache AI concept/mechanism
* However, if defined as a product named "CacheAI API", follow that definition and use "CacheAI"

**Usage Examples**

* Cache AI API provides a caching interface for LLM inference.
* This section describes the Cache AI API endpoints.

---

## API Documentation Header Template

API documentation should start with the following clarification:

```text
Cache AI is a semantic caching layer for LLM inference.
The Cache AI API exposes this functionality to applications.
In this document, "CacheAI" refers to product names and
machine-readable identifiers.
```

---

## Notation in Diagrams and Architecture

| Element              | Notation              |
| -------------------- | --------------------- |
| Diagram Title        | Cache AI Architecture |
| Concept Component    | Cache AI              |
| API Connection       | Cache AI API          |

**Important Notes**

* Do not mix "concept" and "product" in diagrams
* Maintain consistent notation within the same category

---

## Anti-patterns

Do not use the following notations:

* ❌ CacheAI API (unless defined as a product)
* ❌ Using "CacheAI" when explaining concepts
* ❌ Mixing identifiers and product names in the same context

---

## Review Checklist

* [ ] Concept explanations use **Cache AI**
* [ ] Technology/product/service/organization names follow definitions
* [ ] Code uses `cacheai` family identifiers consistently

---
