# **ElderCore RPG**

* Projeto em fase inicial, deixe sua estrela e espere por atualizações futuras

Bem-vindo ao ElderCore RPG, um projeto solo forjado nas sombras e alimentado pela paixão por *dark fantasy* e jogabilidade desafiadora. Aqui, cada linha de código é uma runa antiga, cada personagem, uma alma forjada em batalhas épicas.

---

## ✨ Visão Geral

ElderCore é um motor de RPG *turn-based* e modular, pensado entusiastas que amam mergulhar em histórias profundas e sombrias, enquanto desfrutam de uma interface muito bem trabalhada. Ele oferece:

* **Carga dinâmica de personagens** a partir de arquivos JSON.
* **Sistema de combate** baseado no `CombatLoop`, pronto para monstros e inimigos variados.
* **Classes extensíveis**: Duelist, Werebeast, Healer e muito mais.
* **Menu interativo no terminal** com detalhes personalizáveis de exibição.

Tudo isso com foco em organização, clareza e facilidade de expansão.

---

## ⚙️ Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/eldercore.git
   cd eldercore
   ```
2. Instale as dependências:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate para Windows
   pip install -r requirements.txt
   ```

---

## 🚀 Como usar

1. Prepare seus personagens em `rpg/configs/chars.json` seguindo o exemplo padrão.
2. Execute:

   ```bash
   python -m rpg.main
   ```
3. Navegue pelos menus:

   * **1) Fight**: inicie batalhas.
   * **0) Options**: ajuste visibilidade e formato da ficha.
   * **q) Quit**: encerre a jornada.

---

## 🔮 Roadmap

* [ ] **Novos monstros e chefes**: melhor IA e padrões de ataque.
* [ ] **Árvore de habilidades**: evolução de classes com escolhas cruciais.
* [ ] **Sistema de inventário**: armas, poções e artefatos lendários.
* [ ] **Salvamento automático**: checkpoints sombrios e respawns.
* [ ] **Narrativa interativa**: diálogos, escolhas e ramos de história.

Tem sugestões? Abra uma issue ou fork e envie seu PR com rituais arcânicos (código limpo, testes e documentação).

---

## ♻️ Contribuição

Este é um projeto independente e está em constante evolução. Sinta-se à vontade para:

* **Abrir issues** relatando bugs ou ideias.
* **Criar pull requests** com melhorias.
* **Discutir novos recursos** na seção de issues.

A comunidade dark fantasy agradece.

---

## 📝 Licença

Distribuído sob a licença MIT. Sinta-se livre para usar, adaptar e transformar, mas carregue sempre o peso da honra.

---

> "Nas profundezas do código, as sombras dançam ao sabor dos feitiços de cada desenvolvedor. Que sua jornada seja épica e cada debug, uma conquista lendária."
