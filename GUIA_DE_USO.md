# Guia de Uso - LibraryVault

Este guia abrangente explica como utilizar todas as funcionalidades do sistema LibraryVault, tanto para usuários comuns quanto para administradores.

## Índice
1. [Acesso ao Sistema](#acesso-ao-sistema)
2. [Interface do Usuário](#interface-do-usuário)
3. [Gerenciamento de Documentos](#gerenciamento-de-documentos)
4. [Pesquisa Avançada](#pesquisa-avançada)
5. [Funcionalidades para Administradores](#funcionalidades-para-administradores)
6. [Solução de Problemas](#solução-de-problemas)

## Acesso ao Sistema

### Criação de Conta e Login

1. **Acesso inicial**: Navegue até a página inicial do sistema (`http://seu-dominio.com` ou `http://localhost:8000` em ambiente local).

2. **Criação de conta**:
   - Clique em "Registrar" ou "Criar Conta"
   - Preencha os dados solicitados (nome, email, senha)
   - Opcionalmente, você pode usar autenticação via Google ou Microsoft se disponível

3. **Login**:
   - Insira seu nome de usuário/email e senha
   - Alternativamente, use os botões de login social

4. **Recuperação de senha**:
   - Na tela de login, clique em "Esqueci minha senha"
   - Siga as instruções enviadas ao seu email

## Interface do Usuário

### Navegação Principal

A interface do LibraryVault é organizada em seções principais:

- **Dashboard**: Visão geral e estatísticas de uso
- **Meus Documentos**: Documentos enviados por você
- **Biblioteca**: Todos os documentos disponíveis para você
- **Upload**: Área para envio de novos documentos
- **Configurações**: Ajustes de perfil e preferências

### Personalização da Interface

- **Tema**: Alterne entre tema claro e escuro em Configurações > Aparência
- **Idioma**: Selecione seu idioma preferido em Configurações > Idioma
- **Notificações**: Configure suas preferências de notificação em Configurações > Notificações

## Gerenciamento de Documentos

### Upload de Documentos

1. Acesse a seção "Upload" ou clique no botão "+" no canto superior direito
2. Selecione o tipo de documento (texto, imagem, áudio, vídeo)
3. Arraste os arquivos ou clique para selecionar do seu dispositivo
4. Preencha os metadados obrigatórios:
   - Título
   - Descrição
   - Categoria/Tags
   - Organização (se aplicável)
5. Defina as permissões de acesso:
   - Privado (somente você)
   - Compartilhado (usuários ou grupos específicos)
   - Público (todos os usuários do sistema)
6. Clique em "Enviar" e aguarde a confirmação

### Visualização de Documentos

1. Clique em qualquer documento na biblioteca ou na lista de documentos
2. A visualização depende do tipo de arquivo:
   - Documentos de texto: visualizador integrado
   - Imagens: visualizador de imagem com zoom
   - Áudio/Vídeo: player integrado
3. Use os controles na barra lateral para:
   - Baixar o documento
   - Compartilhar (gerar link)
   - Editar metadados
   - Adicionar aos favoritos
   - Excluir (se você for o proprietário)

### Organização de Documentos

- **Coleções**: Crie coleções para agrupar documentos relacionados
  - Acesse "Minhas Coleções" no menu lateral
  - Clique em "Nova Coleção"
  - Adicione documentos à coleção arrastando-os ou usando o botão "Adicionar à coleção"

- **Tags**: Use tags para categorizar seus documentos
  - Adicione tags durante o upload ou edição
  - Filtre documentos por tags na barra de pesquisa

## Pesquisa Avançada

### Métodos de Pesquisa

- **Pesquisa Básica**: Digite termos na barra de pesquisa principal
- **Pesquisa Avançada**: Use a opção "Pesquisa Avançada" para:
  - Filtrar por tipo de documento
  - Filtrar por data de upload
  - Filtrar por proprietário
  - Filtrar por organização
  - Combinar múltiplos critérios

### Pesquisa Semântica

O LibraryVault inclui pesquisa semântica para encontrar documentos por significado, não apenas por palavras-chave:

1. Ative o modo de pesquisa semântica clicando no ícone "Semântica" na barra de pesquisa
2. Digite uma descrição ou pergunta natural
3. O sistema encontrará documentos relevantes mesmo que não contenham exatamente os termos pesquisados

### Histórico de Pesquisa

- Acesse seu histórico de pesquisas recentes clicando no ícone de relógio na barra de pesquisa
- Salve pesquisas frequentes como favoritas clicando no ícone de estrela

## Funcionalidades para Administradores

### Painel Administrativo

1. Acesse o painel administrativo em `/admin/` com credenciais de administrador
2. No painel, você pode:
   - Gerenciar usuários e permissões
   - Monitorar atividades do sistema
   - Configurar integrações
   - Visualizar estatísticas de uso

### Gerenciamento de Usuários

- **Criar usuários**: Adicione novos usuários manualmente
- **Gerenciar permissões**: Defina funções e permissões por usuário ou grupo
- **Organizações**: Crie e gerencie organizações para agrupar usuários

### Configurações do Sistema

- **Armazenamento**: Configure limites de armazenamento por usuário/organização
- **Tipos de arquivo**: Defina quais tipos de arquivo são permitidos
- **Integrações**: Configure conexões com serviços externos
- **Backup**: Agende e gerencie backups do sistema

## Solução de Problemas

### Problemas Comuns

- **Upload falha**: Verifique o tamanho do arquivo e os tipos permitidos
- **Documento não aparece**: Verifique as permissões de acesso
- **Pesquisa não retorna resultados**: Tente termos mais gerais ou verifique a ortografia
- **Reprodução de mídia falha**: Verifique se o formato é suportado pelo seu navegador

### Suporte Técnico

Se encontrar problemas que não consegue resolver:

1. Consulte a base de conhecimento em "Ajuda > Base de Conhecimento"
2. Entre em contato com o suporte técnico em "Ajuda > Contatar Suporte"
3. Forneça detalhes específicos sobre o problema, incluindo:
   - Descrição do problema
   - Passos para reproduzir
   - Capturas de tela (se aplicável)
   - Informações do navegador e sistema operacional

## Recursos Adicionais

- **Tutoriais em vídeo**: Disponíveis em "Ajuda > Tutoriais"
- **Webinars de treinamento**: Acompanhe o calendário em "Ajuda > Treinamentos"
- **Atualizações**: Fique por dentro das novidades em "Ajuda > Notas de Versão"

---

Para mais informações ou suporte técnico, entre em contato com nossa equipe de suporte.
