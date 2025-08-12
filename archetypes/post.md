---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
author: "{{ .Site.Params.author }}"
categories: []
tags: []
featured: ""     # f.eks. "bilde.jpg" i assets/images/
summary: ""
draft: true
---