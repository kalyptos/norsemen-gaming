---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
type: "page"
menu:
  main:
    name: "{{ replace .Name "-" " " | title }}"
    weight: 50   # juster rekkefølge i menyen
---