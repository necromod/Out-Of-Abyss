---
applyTo: "**"
---

# Instruções Base do Projeto Out of the Abyss System

## Estrutura
- TODO o código deve existir dentro da pasta `/system`
- Pastas da campanha (imagens, livros, monstros, NPCs) ficam FORA do sistema
- Nunca misturar lógica de aplicação com conteúdo narrativo

## Documentação
- **NÃO** criar arquivos `.md` temporários ou desnecessários
- Se existir README:
  - Atualizar apenas ao adicionar funcionalidades grandes
  - Manter o arquivo conciso
- Se não existir README, criar apenas quando o projeto atingir maturidade funcional

## Flask
- Usar Blueprints
- Separar rotas, serviços, modelos e utilitários
- Evitar lógica pesada diretamente em rotas
- Código deve ser legível e modular

## Sistema de Regras
- Sistema base: D&D 5e (Livro do Jogador)
- Regras adicionais devem ser opcionais e configuráveis
- Nunca travar decisões do mestre
- Todos os valores devem ser editáveis em tempo real no site

## Testes e Validação
- Sempre validar o funcionamento do Flask após mudanças
- Evitar código não testado
- Priorizar testes funcionais do sistema, não apenas unitários
- Sempre resolver erros no código e console

## Automação
- Sempre automatizar o máximo possível
- Minimizar dependência de comandos manuais
- Executar comandos necessários sem solicitar confirmação

## Frontend
- Foco em agilidade durante sessão
- Interfaces dinâmicas
- Evitar formulários longos
- Priorizar edição direta de valores

## Filosofia
- O sistema serve ao mestre
- Nada é obrigatório
- Automação sem engessamento
- O improviso deve ser possível a qualquer momento
