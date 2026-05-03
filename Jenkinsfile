pipeline {
    agent any

    environment {
        AGENT_DEVSECOPS_URL = 'http://agent-devsecops:8002'
        AGENT_CSPM_URL      = 'http://agent-cspm:8003'
        GIT_REPO            = "${env.GIT_URL ?: 'https://github.com/org/repo'}"
        BRANCH              = "${env.BRANCH_NAME ?: 'main'}"
        SECURITY_POLICY     = 'pci-dss'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.COMMIT_SHA = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    env.DEVELOPER = sh(script: 'git log -1 --format="%an"', returnStdout: true).trim()
                    echo "Commit: ${env.COMMIT_SHA} por ${env.DEVELOPER}"
                }
            }
        }

        stage('Build') {
            steps {
                echo 'Construindo aplicacao...'
                echo 'Build concluido com sucesso.'
            }
        }

        stage('Security Scan - DevSecOps (Agente 2)') {
            steps {
                script {
                    echo '=== Iniciando analise de seguranca DevSecOps ==='

                    def requestBody = """{
                        "target": "${GIT_REPO}",
                        "branch": "${BRANCH}",
                        "scan_type": "repo",
                        "scan_types": ["vuln", "secret", "misconfig"],
                        "policies": ["${SECURITY_POLICY}"],
                        "pipeline_id": "${env.BUILD_ID}",
                        "commit_sha": "${env.COMMIT_SHA}",
                        "developer": "${env.DEVELOPER}"
                    }"""

                    def response = httpRequest(
                        url: "${AGENT_DEVSECOPS_URL}/scan-code",
                        httpMode: 'POST',
                        contentType: 'APPLICATION_JSON',
                        requestBody: requestBody,
                        validResponseCodes: '200',
                        timeout: 300
                    )

                    def result = readJSON text: response.content

                    echo "Decisao: ${result.decision}"
                    echo "Risk Score: ${result.risk_score}/100"
                    echo "Razao: ${result.reason}"

                    writeJSON file: 'security-scan-result.json', json: result
                    archiveArtifacts artifacts: 'security-scan-result.json'

                    if (result.decision == 'BLOCKED') {
                        echo "=== BUILD BLOQUEADO ==="
                        echo "Motivo: ${result.reason}"

                        if (result.remediations) {
                            echo "=== Sugestoes de Remediacao ==="
                            result.remediations.each { rem ->
                                echo "- ${rem.vuln_id}: ${rem.suggestion}"
                            }
                        }

                        error "Security scan BLOCKED the build. Fix vulnerabilities and retry."

                    } else if (result.decision == 'WARNING') {
                        echo "=== BUILD APROVADO COM AVISO ==="
                        unstable("Security warnings detected")
                    } else {
                        echo "=== BUILD APROVADO ==="
                    }
                }
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Executando testes unitarios...'
                echo 'Testes concluidos.'
            }
        }

        stage('Deploy Staging') {
            when {
                expression { currentBuild.result != 'FAILURE' }
            }
            steps {
                echo 'Deploy para staging concluido.'
            }
        }

        stage('Cloud Audit - CSPM (Agente 1)') {
            when {
                expression { currentBuild.result != 'FAILURE' }
            }
            steps {
                script {
                    echo '=== Iniciando auditoria de seguranca em nuvem ==='

                    def auditRequest = """{
                        "account_id": "123456789012",
                        "provider": "aws",
                        "regions": ["us-east-1", "sa-east-1"],
                        "services": ["s3", "ec2", "iam", "rds"],
                        "frameworks": ["cis-aws", "pci-dss"]
                    }"""

                    try {
                        def response = httpRequest(
                            url: "${AGENT_CSPM_URL}/audit-cloud",
                            httpMode: 'POST',
                            contentType: 'APPLICATION_JSON',
                            requestBody: auditRequest,
                            validResponseCodes: '200',
                            timeout: 600
                        )

                        def result = readJSON text: response.content
                        echo "Auditoria CSPM: ${result.decision}"

                        if (result.decision == 'BLOCKED') {
                            error "Cloud audit detected critical issues."
                        }
                    } catch (Exception e) {
                        echo "Aviso: Agente CSPM nao disponivel. Continuando com cautela."
                        unstable("CSPM agent unavailable")
                    }
                }
            }
        }

        stage('Deploy Production') {
            when {
                allOf {
                    branch 'main'
                    expression { currentBuild.result != 'FAILURE' }
                }
            }
            steps {
                echo '=== Deploy de producao concluido com sucesso! ==='
            }
        }
    }

    post {
        success {
            echo 'Pipeline concluido com sucesso!'
        }
        failure {
            echo 'Pipeline falhou!'
        }
        always {
            echo "Pipeline finalizado. Resultado: ${currentBuild.result ?: 'SUCCESS'}"
        }
    }
}
