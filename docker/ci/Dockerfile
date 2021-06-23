ARG PYTHON_VERSION=3.7
FROM python:${PYTHON_VERSION} AS builder

ARG HADOLINT_VERSION=v1.17.1
RUN wget -q -O /usr/bin/hadolint "https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/hadolint-Linux-$(uname -m)" \
  && chmod +x /usr/bin/hadolint \
  && hadolint --version

ARG SHELLCHECK_VERSION=v0.7.1
RUN wget -q -O /tmp/shellcheck.tar.xz "https://github.com/koalaman/shellcheck/releases/download/${SHELLCHECK_VERSION}/shellcheck-${SHELLCHECK_VERSION}.linux.$(uname -m).tar.xz" \
  && tar -xJf /tmp/shellcheck.tar.xz -C /usr/bin --strip-components=1 "shellcheck-${SHELLCHECK_VERSION}/shellcheck" \
  && rm /tmp/shellcheck.tar.xz \
  && shellcheck --version

ARG HELM_VERSION=3.2.1
RUN wget -q "https://get.helm.sh/helm-v${HELM_VERSION}-linux-amd64.tar.gz" \
  && tar xf "helm-v${HELM_VERSION}-linux-amd64.tar.gz" \
  && mv "linux-amd64/helm" /usr/local/bin/helm \
  && chmod +x /usr/local/bin/helm \
  && rm -rf "linux-amd64" "helm-v${HELM_VERSION}-linux-amd64.tar.gz"

ARG KUBEVAL_VERSION=0.14.0
RUN wget -q https://github.com/instrumenta/kubeval/releases/download/${KUBEVAL_VERSION}/kubeval-linux-amd64.tar.gz \
  && tar xf kubeval-linux-amd64.tar.gz \
  && cp kubeval /usr/local/bin \
  && rm kubeval-linux-amd64.tar.gz \
  && kubeval --version

ARG SHFMT_VERSION=3.1.1
RUN wget -q https://github.com/mvdan/sh/releases/download/v${SHFMT_VERSION}/shfmt_v${SHFMT_VERSION}_linux_amd64 \
  && mv shfmt_v${SHFMT_VERSION}_linux_amd64 shfmt \
  && cp shfmt /usr/local/bin \
  && rm shfmt \
  && chmod +x /usr/local/bin/shfmt \
  && shfmt -version

ARG TERRAFORM_VERSION=0.13.5
RUN wget -q https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
  && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
  && cp terraform /usr/local/bin \
  && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
  && terraform --version

COPY docker/ci/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . .

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN find . -type f -regex '.*\.ya?ml' ! -path '*/helm/*' | while read -r file; do \
      if ! yamllint "${file}"; then \
        echo "Failed yamllint: ${file}" >&2; \
        exit 1; \
      fi; \
    done

RUN find . -type f -name Dockerfile | while read -r file; do \
      if ! hadolint "${file}"; then \
        echo "Failed hadolint: ${file}" >&2; \
        exit 1; \
      fi; \
    done

RUN find . -type f -name '*.sh' | while read -r file; do \
      if ! shellcheck "${file}"; then \
        echo "Failed shellcheck: ${file}" >&2; \
        exit 1; \
      fi; \
    done

RUN helm lint --strict ./helm/opwen_cloudserver \
 && helm template ./helm/opwen_cloudserver > helm.yaml \
 && kubeval --ignore-missing-schemas helm.yaml \
 && rm helm.yaml

RUN shfmt -d -i 2 -ci .

RUN terraform fmt -check

RUN terraform validate -no-color