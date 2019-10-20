#! /bin/bash
#
# Build Python 3.x.x from source on CentOS Linux.
# =============================================================================
# Assume env. variable PYTHON_VERSION is defined, e.g. PYTHON_VERSION=3.5.2
# =============================================================================

BUILD_DIR=/usr/src

# Install dependencies needed for python
# =============================================================================

apt-get install -y ca-certificates locales curl wget gcc g++ file make cmake \
    xz-utils mime-support libbz2-dev libc6-dev libdb-dev libexpat1-dev \
    libffi-dev  libncursesw5-dev libreadline-dev libssl-dev libsqlite3-dev \
    libtinfo-dev zlib1g-dev libpcre++-dev default-libmysqlclient-dev \
    tcl-dev tk-dev libgdbm-dev liblzma-dev uuid-dev \
    pkg-config vim less git rsync --no-install-recommends
# Skip PostgreSQL client: libpq-dev

# =============================================================================
# Download and build all binary libraries with dependencies before users.
# =============================================================================

# Download and build sqlite3 *.so $SQLITE_VERSION
# =============================================================================
cd $BUILD_DIR

SQLITE_YEAR=2019
SQLITE_VERSION=3280000

wget https://www.sqlite.org/${SQLITE_YEAR}/sqlite-autoconf-${SQLITE_VERSION}.tar.gz
tar -xzf sqlite-autoconf-${SQLITE_VERSION}.tar.gz
cd sqlite-autoconf-${SQLITE_VERSION}

# spatialite needs R-Tree indexes
export CFLAGS="-DSQLITE_ENABLE_RTREE=1"
./configure
make
make install

rm $BUILD_DIR/sqlite-autoconf-${SQLITE_VERSION}.tar.gz
rm -R $BUILD_DIR/sqlite-autoconf-${SQLITE_VERSION}

cd -

# Download and build python interpreter $PYTHON_VERSION
# =============================================================================
cd $BUILD_DIR

wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-${PYTHON_VERSION}.tgz
tar -xzf Python-${PYTHON_VERSION}.tgz
cd Python-$PYTHON_VERSION

./configure --enable-shared --enable-ipv6 \
	--enable-loadable-sqlite-extensions \
	--with-ensurepip=yes
make
make install

rm $BUILD_DIR/Python-$PYTHON_VERSION.tgz
rm -R $BUILD_DIR/Python-$PYTHON_VERSION

cd -
