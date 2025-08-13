# Guia Rápido de Seletores XPath e CSS

## Seletores XPath

### **a) Como selecionar um elemento por uma tag?**

```xpath
//tag
```

✔ Exemplo: Selecionar todas as `<div>`

```xpath
//div
```

---

### **b) Como selecionar um elemento aninhado em outro elemento por tag?**

```xpath
//pai/filho
```

✔ Exemplo: Selecionar `<p>` dentro de uma `<div>`

```xpath
//div/p
```

🔹 Se quiser buscar `<p>` dentro de **qualquer nível** dentro de `<div>`:

```xpath
//div//p
```

---

### **c) Como selecionar um elemento somente pela classe?**

```xpath
//*[@class="nome-da-classe"]
```

✔ Exemplo: Selecionar todos os elementos com `class="destaque"`

```xpath
//*[@class="destaque"]
```

🔹 Se a classe estiver combinada com outras:

```xpath
//*[contains(@class, "destaque")]
```

---

### **d) Como selecionar um elemento pela tag e classe?**

```xpath
//tag[@class="nome-da-classe"]
```

✔ Exemplo: Selecionar `<p class="destaque">`

```xpath
//p[@class="destaque"]
```

---

### **e) Como selecionar um elemento por um id?**

```xpath
//*[@id="meu-id"]
```

✔ Exemplo: Selecionar um elemento com `id="principal"`

```xpath
//*[@id="principal"]
```

---

### **f) Como selecionar um elemento pela tag e id?**

```xpath
//tag[@id="meu-id"]
```

✔ Exemplo: Selecionar `<section id="conteudo">`

```xpath
//section[@id="conteudo"]
```

---

### **g) Como selecionar um elemento com um atributo específico?**

```xpath
//tag[@atributo="valor"]
```

✔ Exemplo: Selecionar um `<a>` com `href="https://exemplo.com"`

```xpath
//a[@href="https://exemplo.com"]
```

---

### **h) Como selecionar somente os elementos que estão nos nós filhos de uma seleção?**

```xpath
/pai/filho
```

✔ Exemplo: Selecionar `<li>` **somente filhos diretos** de `<ul>`:

```xpath
//ul/li
```

🔹 Se quiser todos os `<li>`, mesmo que estejam em `<ul>` aninhados:

```xpath
//ul//li
```

---

## Seletores CSS

### **a) Como selecionar um elemento por uma tag?**

```css
tag
```

✔ Exemplo: Selecionar todas as `<div>`

```css
div
```

---

### **b) Como selecionar um elemento aninhado em outro elemento por tag?**

```css
pai > filho  /* Somente filhos diretos */
pai filho  /* Em qualquer nível */
```

✔ Exemplo: Selecionar `<p>` dentro de uma `<div>`

```css
div > p  /* Apenas filhos diretos */
div p  /* Em qualquer nível dentro da <div> */
```

---

### **c) Como selecionar um elemento somente pela classe?**

```css
.classe
```

✔ Exemplo: Selecionar todos os elementos com `class="destaque"`

```css
.destaque
```

---

### **d) Como selecionar um elemento pela tag e classe?**

```css
tag.classe
```

✔ Exemplo: Selecionar `<p class="destaque">`

```css
p.destaque
```

---

### **e) Como selecionar um elemento por um id?**

```css
#id
```

✔ Exemplo: Selecionar um elemento com `id="principal"`

```css
#principal
```

---

### **f) Como selecionar um elemento pela tag e id?**

```css
tag#id
```

✔ Exemplo: Selecionar `<section id="conteudo">`

```css
section#conteudo
```

---

### **g) Como selecionar um elemento com um atributo específico?**

```css
[atributo="valor"]
```

✔ Exemplo: Selecionar um `<a>` com `href="https://exemplo.com"`

```css
a[href="https://exemplo.com"]
```

---

### **h) Como selecionar somente os elementos que estão nos nós filhos de uma seleção?**

```css
pai > filho
```

✔ Exemplo: Selecionar `<li>` **somente filhos diretos** de `<ul>`:

```css
ul > li
```

🔹 Se quiser todos os `<li>`, mesmo que estejam em `<ul>` aninhados:

```css
ul li
```

---

Esse guia cobre os principais seletores XPath e CSS para Web Scraping e desenvolvimento front-end! 🚀
