from enum import Enum

MAP_VERSION_TO_INSTALL_DISCORDPY = {
    k:{
        "python": "3.6",
        "install": "python3 -m pip install -U .[voice]",
        "pre_install": [
            "apt-get update && apt-get install -y libffi-dev python3-dev",
            "pip install PyNaCl",
        ],
    }
    for k in ["1.0.0a", "1.4.0a", "1.5.0", "1.5.0a", "1.6.0", "1.6.0a", "1.7.0a"]
}
MAP_VERSION_TO_INSTALL_DISCORDPY.update(
    {
        k:{
            "python": "3.9",
            "install": "python3 -m pip install -U .[voice]",
            "pre_install": [
                "apt-get update && apt-get install -y libffi-dev python3-dev",
                "pip install PyNaCl",
            ]
        }
        for k in ["2.0.0a", "2.1.0a", "2.2.0a", "2.3.0a", "2.4.0a", "2.5.0a"]
    }
)
MAP_VERSION_TO_INSTALL_DBTCORE = {
    k:{
        "python": "3.6",
        "install": "python -m pip install -e .",
        "pre_install": [
            'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
            "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql postgresql-contrib && service postgresql start",
            'export  USER=odoo && su - postgres -c "createuser -s $USER"',
        ],
    }
    for k in ["0.10.2", "0.11.0", "0.12.0", "0.12.1"]
}
MAP_VERSION_TO_INSTALL_DBTCORE.update(
    {
        k:{
            "python": "3.6",
            "install": "pip install -r requirements.txt",
            "pre_install": [
                'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
                "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql postgresql-contrib && service postgresql start",
                'export  USER=odoo && su - postgres -c "createuser -s $USER"',
            ],
        }
        for k in ["0.13.0", "0.14.0"]
    }
)
MAP_VERSION_TO_INSTALL_DBTCORE.update(
    {
        k:{
            "python": "3.6",
            "install": "pip install -r editable_requirements.txt",
            "pre_install": [
                'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
                "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql postgresql-contrib && service postgresql start",
                'export  USER=odoo && su - postgres -c "createuser -s $USER"',
            ],
        }
        for k in ["0.15.0", "0.18.0", "0.19.0"]
    }
)
MAP_VERSION_TO_INSTALL_DBTCORE.update(
    {
        "0.21.0":{
            "python": "3.6",
            "install": "pip install -r dev-requirements.txt -r editable-requirements.txt",
            "pre_install": [
                'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
                "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql postgresql-contrib && service postgresql start",
                'export  USER=odoo && su - postgres -c "createuser -s $USER"',
                "pip install --upgrade pip",
            ],
        }
    }
)
MAP_VERSION_TO_INSTALL_DBTCORE.update(
    {
        k:{
            "python": "3.7",
            "install": "pip install -r dev-requirements.txt -r editable-requirements.txt",
            "pre_install": [
                'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
                "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql postgresql-contrib && service postgresql start",
                'export  USER=odoo && su - postgres -c "createuser -s $USER"',
                "pip install --upgrade pip",
            ]
        }
        for k in ["1.0.0", "1.0.1", "1.0.3", "1.0.5", "1.0.9"]
    }
)
MAP_VERSION_TO_INSTALL_DBTCORE.update(
    {
        k:{
            "python": "3.8",
            "install": "pip install -r dev-requirements.txt -r editable-requirements.txt",
            "pre_install": [
                'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
                "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql postgresql-contrib && service postgresql start",
                'export  USER=odoo && su - postgres -c "createuser -s $USER"',
                "pip install --upgrade pip",
            ]
        }
        for k in ["1.1.2", "1.1.5", "1.4.1", "1.4.4", "1.5.0", "1.5.1", "1.5.2", "1.6.0", "1.6.1", "1.6.5", "1.7.1", "1.7.9", "1.8.0", "1.8.2", "1.8.3"]
    }
)
MAP_VERSION_TO_INSTALL_CAMEL = {
    k:{
        "python": "3.10",
        "install": "pip install -e .",
    }
    for k in ["0.1.0", "0.1.1"]
}
MAP_VERSION_TO_INSTALL_CAMEL.update(
    {
        k:{
            "python": "3.10",
            "install": "pip install -e .[all]"
        }
        for k in ["0.1.2", "0.1.3", "0.1.5.1", "0.1.5.3", "0.1.5.4", "0.1.5.7"]+\
                 ["0.1.6.6", "0.1.6.9", "0.2.0"]
    }
)
MAP_VERSION_TO_INSTALL_SQLFLUFF = {
    k:{
        "python": "3.9",
        "pre_install": [
            "python3 -m pip install -U tox",
            "sed -i 's/types-pkg_resources/types-setuptools/g' requirements_dev.txt",
            "tox -e py39 --devenv .venv",
            "source .venv/bin/activate",
            "pip install -e plugins/sqlfluff-templater-dbt/.",
        ]
    }
    for k in ["0.8.2", "0.9.0", "0.9.1", "0.9.2", "0.9.4", "0.10.0", "0.10.1"]
}
MAP_VERSION_TO_INSTALL_SQLFLUFF.update(
    {
        k:{
            "python": "3.9",
            "pre_install": [
                "pip install -U tox",
                "sed -i 's/types-pkg_resources/types-setuptools/g' requirements_dev.txt",
                "tox -e py39 --devenv .venv",
                "source .venv/bin/activate",
                "pip install -e plugins/sqlfluff-templater-dbt/.",
            ]
        }
        for k in ["0.11.0", "0.11.1", "0.11.2", "0.12.0", "0.13.0", "0.13.1", "0.13.2"]+ \
                 ["1.0.0", "1.1.0", "1.2.1", "1.3.0", "1.3.2", "1.4.2"]+ \
                 ["2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.5", "2.1.0", "2.1.2", "2.3.2", "2.3.2"]+ \
                 ["3.0.3", "3.0.5", "3.0.7", "3.1.0", "3.1.1"]
    }
)
MAP_VERSION_TO_INSTALL_SQLFLUFF.update(
    {
        "3.1.1":{
            "python": "3.9",
            "pre_install": [
                "pip install -U tox",
                "tox -e py39 --devenv .venv",
                "source .venv/bin/activate",
                "pip install -e plugins/sqlfluff-templater-dbt/.",
            ]
        }
    }
)
MAP_VERSION_TO_INSTALL_ANSIBLE = {
    k:{
        "python": "3.10",
        "install": "python3 -m pip install --user -r ./requirements.txt",
        "pre_install": [
            "apt-get update && apt-get install man-db -y",
            "export LC_ALL=C.UTF-8",
            "source ./hacking/env-setup -q",
        ],
    }
    for k in ["2.15.0.dev0", "2.16.0.dev0", "2.17.0.dev0"]
}

MAP_VERSION_TO_INSTALL_PYTORCH = {
    "2.0.0": {
        "python": "3.9",
        "packages": "requirements.txt",
        "pre_install":[
            "conda install -y cudatoolkit==11.8.0",
            "conda install -y cudnn==8.8.0.121",
            "conda install mkl mkl-include cmake -y",
            "conda install -c conda-forge ninjia",
            "conda install -c pytorch magma-cuda*",
        ],
    },
    "1.10.2": {
        "python": "3.9",
        "packages": "requirements.txt",
        "pre_install": [
            "conda install -y cudatoolkit==11.8.0",
            "conda install -y cudnn==8.8.0.121",
            "conda install astunparse numpy pyyaml mkl mkl-include setuptools",
            "conda install -c conda-forge ninjia",
            "conda install cmake cffi typing_extensions future six requests dataclasses -y",
            "conda install -c pytorch magma-cuda*",
        ]
    }
}
MAP_VERSION_TO_INSTALL_ONNX = {
    k: {
        "python":"3.10",
        "install": "pip install -e .",
        "pre_install": [
            "apt-get update && apt-get install -y cmake",
            "pip install protobuf==3.16.0 numpy==1.22.0",
            "export http_proxy=http://172.31.225.7:7897 && export https_proxy=http://172.31.225.7:7897",
            "git clone https://github.com/protocolbuffers/protobuf.git /tmp",
            "cd /tmp && git checkout v3.16.0 && git submodule update --init --recursive && mkdir build_source && cd build_source",
            "cmake ../cmake -Dprotobuf_BUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_SYSCONFDIR=/etc -DCMAKE_POSITION_INDEPENDENT_CODE=ON -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release",
            "make -j$(nproc) && make install",
            "cd /onnx__onnx/ && git config --global --add safe.directory /onnx__onnx/third_party/pybind11 && git submodule update --init --recursive && export CMAKE_ARGS=-DONNX_USE_LITE_PROTO=ON && rm -r /tmp/*",
        ],
    }
    for k in ["1.10", "1.11"]
}
MAP_VERSION_TO_INSTALL_ONNX.update(
    {
        k:{
            "python":"3.9",
            "install": "python setup.py install",
            "pre_install": [
                "apt-get update && apt-get install -y cmake",
                "pip install protobuf==3.16.0 numpy==1.19.5",
                "export http_proxy=http://172.31.225.7:7897 && export https_proxy=http://172.31.225.7:7897",
                "git clone https://github.com/protocolbuffers/protobuf.git /tmp",
                "cd /tmp && git checkout v3.16.0 && git submodule update --init --recursive && mkdir build_source && cd build_source",
                "cmake ../cmake -Dprotobuf_BUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_SYSCONFDIR=/etc -DCMAKE_POSITION_INDEPENDENT_CODE=ON -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release",
                "make -j$(nproc) && make install",
                "cd /onnx__onnx/ && git config --global --add safe.directory /onnx__onnx/third_party/pybind11 && git submodule update --init --recursive && export CMAKE_ARGS=-DONNX_USE_LITE_PROTO=ON && rm -r /tmp/*",
            ],
        }
        for k in ["1.8", "1.9"]
    }
)
MAP_VERSION_TO_INSTALL_ONNX.update(
    {
        k:{
            "python": "3.9",
            "install": "pip install -e .",
            "pre_install": [
                "apt-get update && apt-get install -y cmake",
                "pip install protobuf==3.16.0 numpy==1.21.5",
                "export http_proxy=http://172.31.225.7:7897 && export https_proxy=http://172.31.225.7:7897",
                "git clone https://github.com/protocolbuffers/protobuf.git /tmp",
                "cd /tmp && git checkout v3.16.0 && git submodule update --init --recursive && mkdir build_source && cd build_source",
                "cmake ../cmake -Dprotobuf_BUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_SYSCONFDIR=/etc -DCMAKE_POSITION_INDEPENDENT_CODE=ON -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release",
                "make -j$(nproc) && make install",
                "cd /onnx__onnx/ && git config --global --add safe.directory /onnx__onnx/third_party/pybind11 && git submodule update --init --recursive && export CMAKE_ARGS=-DONNX_USE_LITE_PROTO=ON",
            ],
        }
        for k in ["1.12"]
    }
)
MAP_VERSION_TO_INSTALL_ONNX.update(
    {
        k:{
            "python": "3.9",
            "install": "pip install -e .",
            "pre_install": [
                "apt-get update && apt-get install -y cmake",
                "pip install protobuf==3.20.2 numpy==1.21.5",
                "export http_proxy=http://172.31.225.7:7897 && export https_proxy=http://172.31.225.7:7897",
                "git clone https://github.com/protocolbuffers/protobuf.git /tmp",
                "cd /tmp && git checkout v3.20.2 && git submodule update --init --recursive && mkdir build_source && cd build_source",
                "cmake ../cmake -Dprotobuf_BUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_SYSCONFDIR=/etc -DCMAKE_POSITION_INDEPENDENT_CODE=ON -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release",
                "make -j$(nproc) && make install",
                "cd /onnx__onnx/ && git config --global --add safe.directory /onnx__onnx/third_party/pybind11 && git submodule update --init --recursive && export CMAKE_ARGS=-DONNX_USE_LITE_PROTO=ON && rm -r /tmp/*",
            ],
        }
        for k in ["1.13"]
    }
)
MAP_VERSION_TO_INSTALL_ONNX.update(
    {
        k:{
            "python": "3.9",
            "install": "pip install -e .",
            "pre_install": [
                "apt-get update && apt-get install -y cmake",
                "pip install protobuf==4.21.12 numpy==1.21.5",
                "export http_proxy=http://172.31.225.7:7897 && export https_proxy=http://172.31.225.7:7897",
                "git clone https://github.com/protocolbuffers/protobuf.git /tmp",
                "cd /tmp && git checkout v3.20.2 && git submodule update --init --recursive && mkdir build_source && cd build_source",
                "cmake ../cmake -Dprotobuf_BUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_SYSCONFDIR=/etc -DCMAKE_POSITION_INDEPENDENT_CODE=ON -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release",
                "make -j$(nproc) && make install",
                "cd /onnx__onnx/ && git config --global --add safe.directory /onnx__onnx/third_party/pybind11 && git submodule update --init --recursive && export CMAKE_ARGS=-DONNX_USE_LITE_PROTO=ON && rm -r /tmp/*",
            ],
        }
        for k in ["1.14"]
    }
)
MAP_VERSION_TO_INSTALL_ONNX.update(
    {
        k:{
            "python": "3.10",
            "install": "pip install -e .",
            "pre_install": [
                "apt-get update && apt-get install -y cmake",
                "pip install protobuf==4.21.12 numpy==1.24.3",
                "export http_proxy=http://172.31.225.7:7897 && export https_proxy=http://172.31.225.7:7897",
                "git clone https://github.com/protocolbuffers/protobuf.git /tmp",
                "cd /tmp && git checkout v21.12 && git submodule update --init --recursive && mkdir build_source && cd build_source",
                "cmake ../cmake -Dprotobuf_BUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_SYSCONFDIR=/etc -DCMAKE_POSITION_INDEPENDENT_CODE=ON -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release",
                "make -j$(nproc) && make install",
                "cd /onnx__onnx/ && git config --global --add safe.directory /onnx__onnx/third_party/pybind11 && git submodule update --init --recursive && export CMAKE_ARGS=-DONNX_USE_LITE_PROTO=ON && rm -r /tmp/*",
            ],
        }
        for k in ["1.15", "1.16"]
    }
)
MAP_VERSION_TO_INSTALL_ODOO = {
    k:{
        "python": "2.7",
        "pre_install": [
            "echo '' > /etc/apt/sources.list",
            "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse\" >> /etc/apt/sources.list'",
            "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse\" >> /etc/apt/sources.list'",
            "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse\" >> /etc/apt/sources.list'",
            "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse\" >> /etc/apt/sources.list'",
            "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse\" >> /etc/apt/sources.list'",
            "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse\" >> /etc/apt/sources.list'",
            "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse\" >> /etc/apt/sources.list'",
            "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse\" >> /etc/apt/sources.list'",
            'sed -i "s/\"//g" /etc/apt/sources.list',
            "apt update && apt install -y gnupg lsb-release",
            'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
            'echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list',
            'wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg',
            'apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-9.5 postgresql-contrib-9.5 && service postgresql start',
            'export  USER=odoo && su - postgres -c "createuser -s $USER"',
            'apt-get update && apt-get install -y python2.7-dev libpq-dev libxml2-dev libxslt1-dev libevent-dev libsasl2-dev libldap2-dev',
            'apt-get update && apt-get install -y libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev libopenjp2-7-dev libraqm-dev',
            'apt-get update && apt-get install -y libfribidi-dev libharfbuzz-dev && apt-get install -y tk-dev tcl-dev && pip install -r requirements.txt',
            'apt-get update && apt install -y npm && npm install -g less',
        ],
    }
    for k in ["9.0", "10.0"]
}
MAP_VERSION_TO_INSTALL_ODOO.update(
    {
        "8.0": {
            "python": "2.7",
            "pre_install": [
                "echo '' > /etc/apt/sources.list",
                "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse\" >> /etc/apt/sources.list'",
                'sed -i "s/\"//g" /etc/apt/sources.list',
                "apt update && apt install -y gnupg lsb-release",
                'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
                'echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list',
                'wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg',
                'apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-9.5 postgresql-contrib-9.5 && service postgresql start',
                'export  USER=odoo && su - postgres -c "createuser -s $USER"',
                'apt-get update && apt-get install -y python2.7-dev libpq-dev libxml2-dev libxslt1-dev libevent-dev libsasl2-dev libldap2-dev',
                'apt-get update && apt-get install -y libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev libopenjp2-7-dev libraqm-dev',
                'apt-get update && apt-get install -y libfribidi-dev libharfbuzz-dev && apt-get install -y tk-dev tcl-dev && pip install -r requirements.txt',
                'apt-get update && apt install -y npm && npm install -g less less-plugin-clean-css',
            ],
        }
    }
)
MAP_VERSION_TO_INSTALL_ODOO.update(
    {
        "11.0":{
            "python": "3.5",
            "pre_install": [
                "echo '' > /etc/apt/sources.list",
                "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb https://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse\" >> /etc/apt/sources.list'",
                "sh -c 'echo \"deb-src https://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse\" >> /etc/apt/sources.list'",
                'sed -i "s/\"//g" /etc/apt/sources.list',
                "apt update && apt install -y gnupg lsb-release",
                'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections && echo "tzdata tzdata/Zones/Asia select Hong_Kong" | debconf-set-selections',
                'echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list',
                'wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg',
                'apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-9.5 postgresql-contrib-9.5 && service postgresql start',
                'export USER=odoo && su - postgres -c "createuser -s $USER"',
                'apt-get update && apt-get install -y python3-dev libpq-dev libxml2-dev libxslt1-dev libevent-dev libsasl2-dev libldap2-dev',
                'apt-get update && apt-get install -y libjpeg-dev zlib1g-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev libopenjp2-7-dev libraqm-dev',
                'apt-get update && apt-get install -y --fix-missing libfribidi-dev libharfbuzz-dev && apt-get install -y --fix-missing tk-dev tcl-dev && pip install -r requirements.txt',
                'apt-get update && apt install -y npm && npm install -g less',
            ],
        }
    }
)
MAP_VERSION_TO_INSTALL_CCXT = {
    k: {
        "python": "3.9",
        "pre_install": [
            "apt-get update && apt-get install -y curl",
            "curl -fsSL https://deb.nodesource.com/setup_18.x | bash -",
            "apt-get install -y nodejs",
            "pip install requests aiohttp ruff tox",
            'echo "tzdata tzdata/Areas select Asia" | debconf-set-selections',
            "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y php",
            "wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.13.1.tar.gz",
            "tar -xzvf libiconv-1.13.1.tar.gz && cd libiconv-1.13.1 && ./configure --prefix=/usr/local",
            "make -j8 && make install",
            "ln -s /usr/local/lib/libiconv.so /usr/lib && ln -s /usr/local/lib/libiconv.so.2 /usr/lib/libiconv.so.2",
            "rm -rf libiconv-1.13.1.tar.gz libiconv-1.13.1",
            "apt-get update && apt-get install -y php-gmp",
            "apt-get update && apt-get install -y libpcre3 libpcre3-dev",
            "apt-get update && apt-get install -y ca-certificates libc6 libgcc-s1 libgssapi-krb5-2 libicu70 liblttng-ust1 libssl3 libstdc++6 libunwind8 zlib1g",
            "wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh && chmod +x ./dotnet-install.sh && ./dotnet-install.sh --channel 2.0",
            "export DOTNET_ROOT=$HOME/.dotnet && export PATH=$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools",
            "rm dotnet-install.sh",
            "npm config set proxy=http://172.31.225.7:7897 && npm config set https_proxy=http://172.31.225.7:7897",
            "npm install",
            "npm run build -y",
        ]
    }
    for k in ["2.8.24"]
}
MAP_VERSION_TO_INSTALL_LANGCHAIN = {
    k: {
        "python": "3.9",
        "pre_install":[
            "pip install poetry==1.4.0",
            "poetry config virtualenvs.prefer-active-python true && poetry install -E all --with dev",
        ],
    }
    for k in ["0.0.123", "0.0.137", "0.0.142", "0.0.147", "0.0.169", "0.0.170"]+ \
             ["0.0.171", "0.0.173", "0.0.174", "0.0.179", "0.0.180", "0.0.183"]+ \
             ["0.0.186", "0.0.189", "0.0.190", "0.0.194"]
}
MAP_VERSION_TO_INSTALL_SKLEARN = {
    k: {
        "python": "3.6",
        "packages": "numpy scipy cython pytest pandas matplotlib",
        "install": "pip install -v --no-use-pep517 --no-build-isolation -e .",
        "arch_specific_packages": {
            "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
        },
        "pip_packages": [
            "numpy==1.19.2",
            "scipy==1.5.2",
        ],
    }
    for k in ["0.20", "0.21", "0.22"]
}
MAP_VERSION_TO_INSTALL_SKLEARN.update(
    {
        k: {
            "python": "3.9",
            "packages": "numpy scipy cython pytest pandas matplotlib joblib threadpoolctl",
            "install": "pip install -v --no-use-pep517 --no-build-isolation -e .",
            "arch_specific_packages": {
                "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            },
        }
        for k in ["1.3", "1.4"]
    }
)

MAP_VERSION_TO_INSTALL_FLASK = {
    "2.0": {
        "python": "3.9",
        "packages": "requirements.txt",
        "install": "pip install -e .",
        "pip_packages": [
            "Werkzeug==2.3.7",
            "Jinja2==3.0.1",
            "itsdangerous==2.1.2",
            "click==8.0.1",
            "MarkupSafe==2.1.3",
        ],
    },
    "2.1": {
        "python": "3.10",
        "packages": "requirements.txt",
        "install": "pip install -e .",
        "pip_packages": [
            "click==8.1.3",
            "itsdangerous==2.1.2",
            "Jinja2==3.1.2",
            "MarkupSafe==2.1.1",
            "Werkzeug==2.3.7",
        ],
    },
}
MAP_VERSION_TO_INSTALL_FLASK.update(
    {
        k: {
            "python": "3.11",
            "packages": "requirements.txt",
            "install": "pip install -e .",
            "pip_packages": [
                "click==8.1.3",
                "itsdangerous==2.1.2",
                "Jinja2==3.1.2",
                "MarkupSafe==2.1.1",
                "Werkzeug==2.3.7",
            ],
        }
        for k in ["2.2", "2.3"]
    }
)

MAP_VERSION_TO_INSTALL_DJANGO = {
    k: {
        "python": "3.5",
        "packages": "requirements.txt",
        "install": "python setup.py install",
    }
    for k in ["1.7", "1.8", "1.9", "1.10", "1.11", "2.0", "2.1", "2.2"]
}
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {"python": "3.5", "install": "python setup.py install"}
        for k in ["1.4", "1.5", "1.6"]
    }
)
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {
            "python": "3.6",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
        }
        for k in ["3.0", "3.1", "3.2"]
    }
)
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {
            "python": "3.8",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
        }
        for k in ["4.0"]
    }
)
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {
            "python": "3.9",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
        }
        for k in ["4.1", "4.2"]
    }
)
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {
            "python": "3.11",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
        }
        for k in ["5.0"]
    }
)
for k in ["2.2", "3.0", "3.1"]:
    MAP_VERSION_TO_INSTALL_DJANGO[k].update(
        {"env_vars_test": { "LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8" }}
    )

MAP_VERSION_TO_INSTALL_REQUESTS = {
    k: {"python": "3.9", "packages": "pytest", "install": "python -m pip install ."}
    for k in
        ["0.7", "0.8", "0.9", "0.11", "0.13", "0.14", "1.1", "1.2", "2.0", "2.2"] + \
        ["2.3", "2.4", "2.5", "2.7", "2.8", "2.9", "2.10", "2.11", "2.12", "2.17"] + \
        ["2.18", "2.19", "2.22", "2.26", "2.25", "2.27", "3.0"]
}

MAP_VERSION_TO_INSTALL_SEABORN = {
    k: {
        "python": "3.9",
        "install": "pip install -e .",
        "pip_packages": [
            "contourpy==1.1.0",
            "cycler==0.11.0",
            "fonttools==4.42.1",
            "importlib-resources==6.0.1",
            "kiwisolver==1.4.5",
            "matplotlib==3.7.2",
            "numpy==1.25.2",
            "packaging==23.1",
            "pandas==2.1.0",
            "pillow==10.0.0",
            "pyparsing==3.0.9",
            "pytest",
            "python-dateutil==2.8.2",
            "pytz==2023.3.post1",
            "scipy==1.11.2",
            "six==1.16.0",
            "tzdata==2023.1",
            "zipp==3.16.2",
        ],
    }
    for k in ["0.11"]
}
MAP_VERSION_TO_INSTALL_SEABORN.update(
    {
        k: {
            "python": "3.9",
            "install": "pip install -e .[dev]",
            "pip_packages": [
                "contourpy==1.1.0",
                "cycler==0.11.0",
                "fonttools==4.42.1",
                "importlib-resources==6.0.1",
                "kiwisolver==1.4.5",
                "matplotlib==3.7.2",
                "numpy==1.25.2",
                "packaging==23.1",
                "pandas==2.1.0",
                "pillow==10.0.0",
                "pyparsing==3.0.9",
                "python-dateutil==2.8.2",
                "pytz==2023.3.post1",
                "scipy==1.11.2",
                "six==1.16.0",
                "tzdata==2023.1",
                "zipp==3.16.2",
            ],
        } for k in ["0.12", "0.13"]
    }
)

MAP_VERSION_TO_INSTALL_PYTEST = {
    k: {
        "python": "3.9",
        "install": "pip install -e ."
    } for k in [
        '4.4','4.5','4.6','5.0','5.1','5.2','5.3','5.4',
        '6.0','6.2','6.3','7.0','7.1','7.2','7.4','8.0'
    ]
}
MAP_VERSION_TO_INSTALL_PYTEST["4.4"]["pip_packages"] = [
    "atomicwrites==1.4.1", "attrs==23.1.0", "more-itertools==10.1.0",
    "pluggy==0.13.1", "py==1.11.0", "setuptools==68.0.0", "six==1.16.0",]
MAP_VERSION_TO_INSTALL_PYTEST["4.5"]["pip_packages"] = [
    "atomicwrites==1.4.1", "attrs==23.1.0", "more-itertools==10.1.0",
    "pluggy==0.11.0", "py==1.11.0", "setuptools==68.0.0", "six==1.16.0", "wcwidth==0.2.6"]
MAP_VERSION_TO_INSTALL_PYTEST["4.6"]["pip_packages"] = [
    "atomicwrites==1.4.1", "attrs==23.1.0", "more-itertools==10.1.0",
    "packaging==23.1", "pluggy==0.13.1", "py==1.11.0", "six==1.16.0", "wcwidth==0.2.6"]
for k in ["5.0", "5.1", "5.2"]:
    MAP_VERSION_TO_INSTALL_PYTEST[k]["pip_packages"] = [
        "atomicwrites==1.4.1", "attrs==23.1.0", "more-itertools==10.1.0",
        "packaging==23.1", "pluggy==0.13.1", "py==1.11.0", "wcwidth==0.2.6"]
MAP_VERSION_TO_INSTALL_PYTEST["5.3"]["pip_packages"] = [
    "attrs==23.1.0", "more-itertools==10.1.0", "packaging==23.1",
    "pluggy==0.13.1", "py==1.11.0", "wcwidth==0.2.6"]
MAP_VERSION_TO_INSTALL_PYTEST["5.4"]["pip_packages"] = [
    "py==1.11.0", "packaging==23.1", "attrs==23.1.0",
    "more-itertools==10.1.0", "pluggy==0.13.1"]
MAP_VERSION_TO_INSTALL_PYTEST["6.0"]["pip_packages"] = [
    "attrs==23.1.0", "iniconfig==2.0.0", "more-itertools==10.1.0",
    "packaging==23.1", "pluggy==0.13.1", "py==1.11.0", "toml==0.10.2"]
for k in ["6.2", "6.3"]:
    MAP_VERSION_TO_INSTALL_PYTEST[k]["pip_packages"] = [
        "attrs==23.1.0", "iniconfig==2.0.0", "packaging==23.1",
        "pluggy==0.13.1", "py==1.11.0", "toml==0.10.2"]
MAP_VERSION_TO_INSTALL_PYTEST["7.0"]["pip_packages"] = [
    "attrs==23.1.0", "iniconfig==2.0.0", "packaging==23.1",
    "pluggy==0.13.1", "py==1.11.0"]
for k in ["7.1", "7.2"]:
    MAP_VERSION_TO_INSTALL_PYTEST[k]["pip_packages"] = [
        "attrs==23.1.0", "iniconfig==2.0.0", "packaging==23.1",
        "pluggy==0.13.1", "py==1.11.0", "tomli==2.0.1"]
MAP_VERSION_TO_INSTALL_PYTEST["7.4"]["pip_packages"] = [
    "iniconfig==2.0.0", "packaging==23.1", "pluggy==1.3.0",
    "exceptiongroup==1.1.3", "tomli==2.0.1"]
MAP_VERSION_TO_INSTALL_PYTEST["8.0"]["pip_packages"] = [
    "iniconfig==2.0.0", "packaging==23.1", "pluggy==1.3.0",
    "exceptiongroup==1.1.3", "tomli==2.0.1"]

MAP_VERSION_TO_INSTALL_MATPLOTLIB = {
    k: {
        "python": "3.11",
        "packages": "environment.yml",
        "install": "python -m pip install -e .",
        "pip_packages": [
            "contourpy==1.1.0",
            "cycler==0.11.0",
            "fonttools==4.42.1",
            "kiwisolver==1.4.5",
            "numpy==1.25.2",
            "packaging==23.1",
            "pillow==10.0.0",
            "pyparsing==3.0.9",
            "python-dateutil==2.8.2",
            "six==1.16.0",
            "setuptools==68.1.2",
            "setuptools-scm==7.1.0",
            "typing-extensions==4.7.1",
        ],
        "arch_specific_packages": {
            "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
        }
    }
    for k in ["3.5", "3.6", "3.7"]
}
MAP_VERSION_TO_INSTALL_MATPLOTLIB.update(
    {
        k: {
            "python": "3.8",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
            "arch_specific_packages": {
                "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            }
        }
        for k in ["3.1", "3.2", "3.3", "3.4"]
    }
)
MAP_VERSION_TO_INSTALL_MATPLOTLIB.update(
    {
        k: {
            "python": "3.7",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
            "arch_specific_packages": {
                "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            }
        }
        for k in ["3.0"]
    }
)
MAP_VERSION_TO_INSTALL_MATPLOTLIB.update(
    {
        k: {
            "python": "3.5",
            "install": "python setup.py build; python setup.py install",
            "arch_specific_packages": {
                "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            }
        }
        for k in ["2.0", "2.1", "2.2", "1.0", "1.1", "1.2", "1.3", "1.4", "1.5"]
    }
)

MAP_VERSION_TO_INSTALL_SPHINX = {
    k: {
        "python": "3.9",
        "pip_packages": ["tox"],
        "install": "pip install -e .[test]",
        "pre_install": ["sed -i 's/pytest/pytest -rA/' tox.ini"],
        "arch_specific_packages": {
            "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            "x86_64": "gxx_linux-64 gcc_linux-64 make",
        }
    } for k in
        ["1.5", "1.6", "1.7", "1.8", "2.0", "2.1", "2.2", "2.3", "2.4", "3.0"] + \
        ["3.1", "3.2", "3.3", "3.4", "3.5", "4.0", "4.1", "4.2", "4.3", "4.4"] + \
        ["4.5", "5.0", "5.1", "5.2", "5.3", "6.0", "6.2", "7.0", "7.1", "7.2"]
}
for k in ["3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "4.0", "4.1", "4.2", "4.3", "4.4"]:
    MAP_VERSION_TO_INSTALL_SPHINX[k][
        "pre_install"
    ].extend([
        "sed -i 's/Jinja2>=2.3/Jinja2<3.0/' setup.py",
        "sed -i 's/sphinxcontrib-applehelp/sphinxcontrib-applehelp<=1.0.7/' setup.py",
        "sed -i 's/sphinxcontrib-devhelp/sphinxcontrib-devhelp<=1.0.5/' setup.py",
        "sed -i 's/sphinxcontrib-qthelp/sphinxcontrib-qthelp<=1.0.6/' setup.py",
        "sed -i 's/alabaster>=0.7,<0.8/alabaster>=0.7,<0.7.12/' setup.py",
        'sed -i "s/\'packaging\',/\'packaging\', \'markupsafe<=2.0.1\',/" setup.py',
    ])
    if k in ["4.2", "4.3", "4.4"]:
        MAP_VERSION_TO_INSTALL_SPHINX[k]["pre_install"].extend([
            "sed -i 's/sphinxcontrib-htmlhelp>=2.0.0/sphinxcontrib-htmlhelp>=2.0.0,<=2.0.4/' setup.py",
            "sed -i 's/sphinxcontrib-serializinghtml>=1.1.5/sphinxcontrib-serializinghtml>=1.1.5,<=1.1.9/' setup.py",
        ])
    elif k == "4.1":
        MAP_VERSION_TO_INSTALL_SPHINX[k]["pre_install"].extend([
            (
                "grep -q 'sphinxcontrib-htmlhelp>=2.0.0' setup.py && "
                "sed -i 's/sphinxcontrib-htmlhelp>=2.0.0/sphinxcontrib-htmlhelp>=2.0.0,<=2.0.4/' setup.py || "
                "sed -i 's/sphinxcontrib-htmlhelp/sphinxcontrib-htmlhelp<=2.0.4/' setup.py"
            ),
            (
                "grep -q 'sphinxcontrib-serializinghtml>=1.1.5' setup.py && "
                "sed -i 's/sphinxcontrib-serializinghtml>=1.1.5/sphinxcontrib-serializinghtml>=1.1.5,<=1.1.9/' setup.py || "
                "sed -i 's/sphinxcontrib-serializinghtml/sphinxcontrib-serializinghtml<=1.1.9/' setup.py"
            )
        ])
    else:
        MAP_VERSION_TO_INSTALL_SPHINX[k]["pre_install"].extend([
            "sed -i 's/sphinxcontrib-htmlhelp/sphinxcontrib-htmlhelp<=2.0.4/' setup.py",
            "sed -i 's/sphinxcontrib-serializinghtml/sphinxcontrib-serializinghtml<=1.1.9/' setup.py",
        ])


MAP_VERSION_TO_INSTALL_ASTROPY = {
    k: {
        "python": "3.9",
        "install": "pip install -e .[test]",
        "pip_packages": [
            "attrs==23.1.0", "exceptiongroup==1.1.3", "execnet==2.0.2", "hypothesis==6.82.6",
            "iniconfig==2.0.0", "numpy==1.25.2", "packaging==23.1", "pluggy==1.3.0",
            "psutil==5.9.5", "pyerfa==2.0.0.3", "pytest-arraydiff==0.5.0", "pytest-astropy-header==0.2.2",
            "pytest-astropy==0.10.0", "pytest-cov==4.1.0", "pytest-doctestplus==1.0.0", "pytest-filter-subpackage==0.1.2",
            "pytest-mock==3.11.1", "pytest-openfiles==0.5.0", "pytest-remotedata==0.4.0", "pytest-xdist==3.3.1",
            "pytest==7.4.0", "PyYAML==6.0.1", "setuptools==68.0.0", "sortedcontainers==2.4.0", "tomli==2.0.1",
        ],
    }
    for k in
        ["0.1", "0.2", "0.3", "0.4", "1.1", "1.2", "1.3", "3.0", "3.1", "3.2"] + \
        ["4.1", "4.2", "4.3", "5.0", "5.1", "5.2"]
}

MAP_VERSION_TO_INSTALL_SYMPY = {
    k: {
        "python": "3.9",
        "packages": "mpmath flake8",
        "pip_packages": ["mpmath==1.3.0", "flake8-comprehensions"],
        "install": "pip install -e .",
    }
    for k in
        ["0.7", "1.0", "1.1", "1.10", "1.11", "1.12", "1.2", "1.4", "1.5", "1.6"] + \
        ["1.7", "1.8", "1.9"]
}
MAP_VERSION_TO_INSTALL_SYMPY.update(
    {
        k: {
            "python": "3.9",
            "packages": "requirements.txt",
            "install": "pip install -e .",
            "pip_packages": ["mpmath==1.3.0"],
        }
        for k in ["1.13"]
    }
)

MAP_VERSION_TO_INSTALL_PYLINT = {
    k: {"python": "3.9", "packages": "requirements.txt", "install": "pip install -e ."}
    for k in ["2.10", "2.11", "2.13", "2.14", "2.15", "2.16", "2.17", "2.8", "2.9", "3.0"]
}
MAP_VERSION_TO_INSTALL_PYLINT.update({
    k: {**MAP_VERSION_TO_INSTALL_PYLINT[k], "pip_packages": [
        "astroid==3.0.0a6"
    ]} for k in ['3.0']})

MAP_VERSION_TO_INSTALL_XARRAY = {
    k: {
        "python": "3.10",
        "packages": "environment.yml",
        "install": "pip install -e .",
        "pip_packages": [
            "numpy==1.25.2",
            "packaging==23.1",
            "pandas==1.5.3",
            "pytest==8.1.1",
            "python-dateutil==2.8.2",
            "pytz==2023.3",
            "six==1.16.0",
        ],
        "no_use_env": True,
    }
    for k in ["0.12", "0.18", "0.19", "0.20", "2022.03", "2022.06", "2022.09"]
}
'''
MAP_VERSION_TO_INSTALL_SQLFLUFF = {
    k: {
        "python": "3.9",
        "packages": "requirements.txt",
        "install": "pip install -e .",
    }
    for k in [
        '0.10', '0.11', '0.12', '0.13', '0.4', '0.6', '0.8', '0.9',
        '1.1', '1.2', '1.3', '1.4', '2.0', '2.1', '2.2'
    ]
}
'''
MAP_VERSION_TO_INSTALL_PYVISTA = {
    k: {
        "python": "3.9",
        "install": "pip install -e .",
        "pip_packages": ["pytest"],
    }
    for k in ['0.20', '0.21', '0.22', '0.23']
}
MAP_VERSION_TO_INSTALL_PYVISTA.update({
    k: {
        "python": "3.9",
        "packages": "requirements.txt",
        "install": "pip install -e .",
        "pip_packages": ["pytest"],
    }
    for k in [
        '0.24', '0.25', '0.26', '0.27', '0.28', '0.29', '0.30', '0.31',
        '0.32', '0.33', '0.34', '0.35', '0.36', '0.37', '0.38', '0.39',
        '0.40', '0.41', '0.42', '0.43'
    ]
})

MAP_VERSION_TO_INSTALL_ASTROID = {
    k: {
        "python": "3.9",
        "install": "pip install -e .",
        "pip_packages": ["pytest"],
    }
    for k in ['2.10', '2.12', '2.13', '2.14', '2.15', '2.5', '2.6', '2.7', '2.9', '3.0']
}
for k in ["2.5", "2.6"]:
    MAP_VERSION_TO_INSTALL_ASTROID[k]["pip_packages"] = [
        "lazy_object_proxy==1.9.0", "wrapt==1.12.1"]
for k in ["2.9", "2.10"]:
    MAP_VERSION_TO_INSTALL_ASTROID[k]["pip_packages"] = [
        "lazy_object_proxy==1.9.0", "wrapt==1.13.3",
        "typing-extensions==4.8.0", "setuptools==68.0.0"]
for k in ["2.12", "2.13", "2.14", "2.15"]:
    MAP_VERSION_TO_INSTALL_ASTROID[k]["pip_packages"] = [
        "lazy_object_proxy==1.9.0", "wrapt==1.15.0", "typing-extensions==4.8.0"]
MAP_VERSION_TO_INSTALL_ASTROID["2.7"]["pip_packages"] = [
    "lazy_object_proxy==1.9.0", "wrapt==1.12.1", "typing-extensions==4.8.0"]
MAP_VERSION_TO_INSTALL_ASTROID["3.0"]["pip_packages"] = ["typing-extensions==4.8.0"]


MAP_VERSION_TO_INSTALL_MARSHMALLOW = {
    k: {
        "python": "3.9",
        "install": "pip install -e '.[dev]'",
    }
    for k in ['2.18', '2.19', '2.20', '3.0', '3.12', '3.19', '3.9']
}

MAP_VERSION_TO_INSTALL_PVLIB = {
    k: {
        "python": "3.9",
        "install": "pip install -e .[all]",
        "packages": "pandas scipy",
        "pip_packages": ["jupyter", "ipython", "matplotlib", "pytest", "flake8"]
    }
    for k in ['0.5', '0.6', '0.7', '0.8', '0.9']
}

MAP_VERSION_TO_INSTALL_PYDICOM = {
    k: {
        "python": "3.6",
        "install": "pip install -e .",
        "packages": "numpy"
    }
    for k in ['1.2', '1.3', '1.4', '2.0', '2.1', '2.2', '2.3']
}
MAP_VERSION_TO_INSTALL_PYDICOM.update({
    k: {**MAP_VERSION_TO_INSTALL_PYDICOM[k], "python": "3.8"}
    for k in ['1.4', '2.0']})
MAP_VERSION_TO_INSTALL_PYDICOM.update({
    k: {**MAP_VERSION_TO_INSTALL_PYDICOM[k], "python": "3.9"}
    for k in ['2.1', '2.2']})
MAP_VERSION_TO_INSTALL_PYDICOM.update({
    k: {**MAP_VERSION_TO_INSTALL_PYDICOM[k], "python": "3.10"}
    for k in ['2.3']})

MAP_VERSION_TO_INSTALL_HUMANEVAL= {k: { "python": "3.9" } for k in ['1.0']}

# Constants - Task Instance Instllation Environment
MAP_VERSION_TO_INSTALL = {
    "astropy/astropy": MAP_VERSION_TO_INSTALL_ASTROPY,
    "ansible/ansible": MAP_VERSION_TO_INSTALL_ANSIBLE,
    "django/django": MAP_VERSION_TO_INSTALL_DJANGO,
    "matplotlib/matplotlib": MAP_VERSION_TO_INSTALL_MATPLOTLIB,
    "marshmallow-code/marshmallow": MAP_VERSION_TO_INSTALL_MARSHMALLOW,
    "mwaskom/seaborn": MAP_VERSION_TO_INSTALL_SEABORN,
    "pallets/flask": MAP_VERSION_TO_INSTALL_FLASK,
    "psf/requests": MAP_VERSION_TO_INSTALL_REQUESTS,
    "pvlib/pvlib-python": MAP_VERSION_TO_INSTALL_PVLIB,
    "pydata/xarray": MAP_VERSION_TO_INSTALL_XARRAY,
    "pydicom/pydicom": MAP_VERSION_TO_INSTALL_PYDICOM,
    "pylint-dev/astroid": MAP_VERSION_TO_INSTALL_ASTROID,
    "pylint-dev/pylint": MAP_VERSION_TO_INSTALL_PYLINT,
    "pytest-dev/pytest": MAP_VERSION_TO_INSTALL_PYTEST,
    "pyvista/pyvista": MAP_VERSION_TO_INSTALL_PYVISTA,
    "scikit-learn/scikit-learn": MAP_VERSION_TO_INSTALL_SKLEARN,
    "sphinx-doc/sphinx": MAP_VERSION_TO_INSTALL_SPHINX,
    "swe-bench/humaneval": MAP_VERSION_TO_INSTALL_HUMANEVAL,
    "sympy/sympy": MAP_VERSION_TO_INSTALL_SYMPY,
    "pytorch/pytorch": MAP_VERSION_TO_INSTALL_PYTORCH,
    "onnx/onnx": MAP_VERSION_TO_INSTALL_ONNX,
    "odoo/odoo": MAP_VERSION_TO_INSTALL_ODOO,
    "ccxt/ccxt": MAP_VERSION_TO_INSTALL_CCXT,
    "langchain-ai/langchain": MAP_VERSION_TO_INSTALL_LANGCHAIN,
    "sqlfluff/sqlfluff": MAP_VERSION_TO_INSTALL_SQLFLUFF,
    'camel-ai/camel': MAP_VERSION_TO_INSTALL_CAMEL,
    "Rapptz/discord.py": MAP_VERSION_TO_INSTALL_DISCORDPY,
    "dbt-labs/dbt-core": MAP_VERSION_TO_INSTALL_DBTCORE,
}

# Constants - Repository Specific Installation Instructions
MAP_REPO_TO_INSTALL = {}

# Constants - Task Instance Test Frameworks
TEST_PYTEST = "pytest --no-header -rA --tb=no -p no:cacheprovider"
MAP_REPO_TO_TEST_FRAMEWORK = {
    "astropy/astropy": TEST_PYTEST,
    "dbt-labs/dbt-core": TEST_PYTEST,
    "django/django": "./tests/runtests.py --verbosity 2",
    "huggingface/transformers": TEST_PYTEST,
    "marshmallow-code/marshmallow": TEST_PYTEST,
    "matplotlib/matplotlib": TEST_PYTEST,
    "mwaskom/seaborn": "pytest --no-header -rA",
    "pallets/flask": TEST_PYTEST,
    "psf/requests": TEST_PYTEST,
    "pvlib/pvlib-python": TEST_PYTEST,
    "pydata/xarray": TEST_PYTEST,
    "pydicom/pydicom": TEST_PYTEST,
    "pylint-dev/astroid": TEST_PYTEST,
    "pylint-dev/pylint": TEST_PYTEST,
    "pytest-dev/pytest": "pytest -rA",
    "pyvista/pyvista": TEST_PYTEST,
    "scikit-learn/scikit-learn": TEST_PYTEST,
    "sphinx-doc/sphinx": "tox -epy39 -v --",
    "swe-bench/humaneval": "python",
    "sympy/sympy": "bin/test -C --verbose",
    "ansible/ansible": TEST_PYTEST,
    "pytorch/pytorch": TEST_PYTEST,
    "onnx/onnx": TEST_PYTEST,
    "odoo/odoo": TEST_PYTEST,
    "ccxt/ccxt": TEST_PYTEST,
    "langchain-ai/longchain": TEST_PYTEST,
    "sqlfluff/sqlfluff": "tox -e py38 -- -k AL02 test",
}

# Constants - Task Instance Requirements File Paths
MAP_REPO_TO_REQS_PATHS = {
    "ansible/ansible": ["requirements.txt"],
    "dbt-labs/dbt-core": ["dev-requirements.txt", "dev_requirements.txt"],
    "django/django": ["tests/requirements/py3.txt"],
    "matplotlib/matplotlib": ["requirements/dev/dev-requirements.txt", "requirements/testing/travis_all.txt"],
    "pallets/flask": ["requirements/dev.txt"],
    "pylint-dev/pylint": ["requirements_test.txt"],
    "pyvista/pyvista": ["requirements_test.txt", 'requirements.txt'],
    "sympy/sympy": ["requirements-dev.txt"],
    "pytorch/pytorch": ["requirements.txt", "requirements-flake8.txt"],
    "onnx/onnx": ["requirements-dev.txt"],
    "langchain-ai/langchain": ["libs/langchain/requirements.txt"],
}

# Constants - Task Instance environment.yml File Paths
MAP_REPO_TO_ENV_YML_PATHS = {
    "matplotlib/matplotlib": ["environment.yml"],
    "pydata/xarray": ["ci/requirements/environment.yml", "environment.yml"],
}

# Constants - Evaluation Keys
KEY_INSTANCE_ID = "instance_id"
KEY_MODEL = "model_name_or_path"
KEY_PREDICTION = "model_patch"

# Constants - Logging
APPLY_PATCH_FAIL = ">>>>> Patch Apply Failed"
APPLY_PATCH_PASS = ">>>>> Applied Patch"
INSTALL_FAIL = ">>>>> Init Failed"
INSTALL_PASS = ">>>>> Init Succeeded"
INSTALL_TIMEOUT = ">>>>> Init Timed Out"
RESET_FAILED = ">>>>> Reset Failed"
TESTS_ERROR = ">>>>> Tests Errored"
TESTS_FAILED = ">>>>> Some Tests Failed"
TESTS_PASSED = ">>>>> All Tests Passed"
TESTS_TIMEOUT = ">>>>> Tests Timed Out"

# Constants - Patch Types
class PatchType(Enum):
    PATCH_GOLD = "gold"
    PATCH_PRED = "pred"
    PATCH_PRED_TRY = "pred_try"
    PATCH_PRED_MINIMAL = "pred_minimal"
    PATCH_PRED_MINIMAL_TRY = "pred_minimal_try"
    PATCH_TEST = "test"

# Constants - Miscellaneous
NON_TEST_EXTS = [".json", ".png", "csv", ".txt", ".md", ".jpg", ".jpeg", ".pkl", ".yml", ".yaml", ".toml"]
SWE_BENCH_URL_RAW = "https://raw.githubusercontent.com/"

# Constants - Repo/Version Mapped to Appropriate Conda Link
MAP_REPO_VERSION_TO_CONDA_LINK = {
    "psf/requests": {
        "2.4": "py39_23.9.0-0",
    },
}

DEFAULT_CONDA_LINK = "py39_23.10.0-1"