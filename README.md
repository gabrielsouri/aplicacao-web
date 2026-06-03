# Aplicação Web (Challenge FIAP + ZUP + StackSpot AI)

Aplicação web simples em Flask que serve de alvo para os agentes de segurança que desenvolvi no Challenge FIAP + ZUP + StackSpot AI, no curso de Defesa Cibernética da FIAP.

> **Aviso importante:** este repositório é intencionalmente vulnerável. Ele existe para que os agentes de segurança tenham o que detectar, classificar e corrigir. Não use este código em produção.

## Contexto

No challenge, desenvolvi dois agentes de segurança integrados a um pipeline de CI/CD:

- **Agente CSPM (Fase 3):** audita ambientes AWS com o Prowler e contextualiza os achados com IA via StackSpot AI.
- **Agente DevSecOps (Fase 4):** escaneia repositórios de código com o Trivy, decide se o build pode seguir com base em políticas de segurança e dispara uma automação de remediação na AWS Lambda quando necessário.

Este repositório é a aplicação que o Agente DevSecOps escaneia. As vulnerabilidades aqui são propositais: são elas que o pipeline detecta e corrige automaticamente.

## O que o scanner encontra (de propósito)

- Dependências desatualizadas no `requirements.txt`, com vulnerabilidades conhecidas.
- Configuração de desenvolvimento insegura no `app.py` (modo debug ligado).
- Imagem base ampla no `Dockerfile`, que carrega muitos pacotes de sistema.

Esses pontos são o material de demonstração do scanner. Em um projeto real, cada um deles seria corrigido.

## Como o pipeline trata isso

Fluxo configurado no `Jenkinsfile`:

1. O Jenkins faz o checkout deste repositório.
2. Chama o Agente DevSecOps, que roda o Trivy e aplica a política de segurança escolhida.
3. Com a política `pci-dss`, o build é bloqueado e o agente lista as remediações.
4. A automação na AWS Lambda abre um Pull Request com as correções, ajustando `requirements.txt`, `Dockerfile` e `k8s/deployment.yaml`.
5. Com a política `default`, o mesmo código é aprovado com um risk score mais baixo.

O `Dockerfile` e o `k8s/deployment.yaml` deste repositório já mostram correções aplicadas por esse fluxo, como execução com usuário sem privilégios, healthcheck e um securityContext endurecido.

## Stack

- Python 3.9 e Flask
- HTML, CSS e JavaScript
- Docker
- Kubernetes (manifesto de deployment)
- Jenkins (pipeline de CI/CD)

## Rotas

- `/` página inicial
- `/config` página de configurações

## Como rodar localmente

Com Python:

```bash
pip install -r requirements.txt
python app.py
```

A aplicação sobe em `http://localhost:5000`.

Com Docker:

```bash
docker build -t webapp .
docker run -p 5000:5000 webapp
```

## Estrutura do projeto

```
.
├── app.py                 # aplicacao Flask
├── requirements.txt       # dependencias (alvo do scan)
├── Dockerfile             # imagem do container
├── Jenkinsfile            # pipeline de CI/CD com os dois agentes
├── Procfile               # configuracao de deploy
├── k8s/
│   └── deployment.yaml    # manifesto Kubernetes
├── static/                # CSS e JavaScript
└── template/              # templates HTML
```

## Sobre o challenge

Projeto desenvolvido para o Challenge FIAP + ZUP + StackSpot AI. O foco foi construir agentes que não apenas detectam problemas de segurança, mas também priorizam o risco e entregam a correção pronta, integrados a um pipeline de CI/CD de ponta a ponta.
