---
title: 'mmh3: A Python extension for MurmurHash3'
tags:
  - Python
  - hash
  - high-performance computing
  - artificial intelligence
  - natural language processing
  - internet of things
  - cybersecurity
authors:
  - name: Hajime Senuma
    orcid: 0000-0001-8542-1768
    affiliation: 1
affiliations:
 - name: University of Tokyo
   index: 1
date: 22 May 2023
bibliography: paper.bib

---

# Summary
This decade has witnessed the rapid evolution of artificial intelligence (AI), notably in the field of natural language processsing (NLP), as represented by the popularity of OpenAI’s ChatGPT. Another important advancement in computer science and engineering is found in the field of the Internet of Things (IoT), a crucial component of ubiquitous computing, as represented by the development of Shodan, the world's first IoT search engine.

Underlying these advancements are high-performance algorithms and data structures that use non-cryptographic hash functions. This type of hash functions is generally characterized by four properties; they are fast, their resulting bits are statistically well-distributed, they have an avalanche effect, meaning a one-bit difference in a key changes at least half of the resulting bits, and they are collision resistant. Because cryptographic strength is not required in these use cases, they can leverage the efficiency of non-cryptographic hash functions.

MurmurHash3 and its test suite, SMHasher, was developed by @appleby_murmurhash3_2011 and is one of the earliest and most continuously popular hash functions specifically designed to implement the characteristics mentioned above.

`mmh3` was launched in 2011 as a Python wrapper for MurmurHash3 and has been maintained ever since. Its API is very simple to use for Python programmers, as it offers both simple one-shot hash functions and hasher classes that allow incremental updating, whose methods are compliant to `hashlib`, a part of the Python Standard Library. The library provides Python wheels (i.e., pre-built binary packages) for immediate use on various platforms, including Linux (x86\_64, aarch64, i686, ppc64le, and s390x), Windows (win32, win\_amd64, and win\_arm64), and macOS (Intel Mac and Apple Silicon). From version 4.0.0, `mmh3` has been published under the MIT License, an OSI-approved permissive open-source license.

As of May 1, 2023, `mmh3` was being downloaded more than 2 million times per month, and it ranks as the 1,027th most downloaded PyPI package (of around 450,000 projects), showing that only 0.23% of the remaining packages in the PyPI ecosystem are more popular [@hugo_van_kemenade_2023_7882688]. According to PePy, as of May 22, 2023, the total downloads of this library exceeded 78 millions.

Libraries and organizations that directly use `mmh3` include Apache Iceberg (an open table format for analytic datasets), PyMilvus (a Python SDK for Milvus, an open-source vector database), Shodan (the world’s first IoT search engine), and pocsuite3 (open-source remote vulnerability testing framework). Those that contain `mmh3` as an indirect dependency include the ChatGPT Retrieval Plugin by OpenAI.

# Statement of need
## AI and High-Performance Computing
AI is one of the most resource-demanding fields in computer science and engineering. To mitigate this problem, various techniques are employed under main systems, in which non-cryptographic hash functions play key roles in a number of algorithms and data structures.

A notable technique is *feature hashing* [@Weinberger2009; @Shi2009]. In its simplest usage, when given a string-indexed data vector, it simply converts the vector into an integer-indexed data vector in which each index is the hash result of the original string index; collision values are simply summed. Despite its simple and intuitive usage, a machine-learning process with feature hashing is statistically guaranteed to be nearly as accurate as its original process. Feature hashing has been shown to be useful for various situations, including K-means clustering [@Senuma2011] and succinct model learning [@Senuma2016].

Other popular techniques that leverage non-cryptographic hash functions include *Bloom Filter* [@Bloom1970], a compact data structure that tests whether an element is a member of a certain set (with false positive matches), and *MinHash* [@Broder1997a], an algorithm that quickly estimates the similarity of two sets.

`mmh3` has appears in various scholarly papers, including a study of Indian language NLP suites [@kakwani_indicnlpsuite_2020] and another about a secure system based on probabilistic structures [@adja_blockchain-based_2021]. It has also appeared in technical books and computer science texts [@gorelick_high_2020; @kumar_probabilistic_2021; @medjedovic_algorithms_2022].

## Internet of Things
`mmh3` is applicable to the IoT field. Shodan uses `mmh3` as its fingerprint for a favicon (i.e., an icon associated with a web page or website) [@shodan_its_2021]. @shodan_we_2020 explained they adopted `mmh3` because it was space efficient and has scalable performance. ZoomEye, another popular IoT search engine, follows Shodan’s convention.

As a result, `mmh3` is considered a useful tool for cybersecurity. For example, @kopriva_hunting_2021 reported a method of discovering possible phishing websites by searching websites with Shodan, whose favicon’s `mmh3` hash value was the same as that of a genuine and trustable one.

Another use case of `mmh3` in this area includes open-source intelligence (OSINT) activities, such as measuring the global popularity of web frameworks and servers, as some users do not change their default favicon settings specified by applications. @faraday_security_understanding_2022 described a method of using `mmh3` and Shodan to approximate the popularity of `Spring`, a Java-based web framework.

# Related software
`PYMMH` [@kihlander_pymmh3_2013] is a pure Python implementation of the MurmurHash3 algorithm. Among various other Python bindings for non-cryptographic hashes, `xxhash` by Yue Du [@du_xxhash_2014] is another popular hash library, featuring xxHash developed by Yan Collet [@collet_xxhash_2012].

# Acknowledgements
The author expresses his deep gratitude to Professor Akiko Aizawa for her helpful comments on this paper. He also appreciates the contributions of individuals to the development and maintenance of `mmh3`. Special thanks go to Dr. Micha Gorelick, who made the first pull request to the project and later introduced the library in her technical book [@gorelick_high_2020].

# References