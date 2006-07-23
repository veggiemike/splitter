MAKEFILE = Makefile

PRODUCT	      =	splitter
VERSION	      =	0.8.0
PACKAGEREV    =	1
DEVTAG	      =	pre
DEVDATE	      =	`date +"%Y%m%d"`

ifeq (${DEVTAG},)
	VERSIONSTRING=${VERSION}
else
	VERSIONSTRING=${VERSION}-${DEVTAG}${DEVDATE}
endif

DISTNAME      =	${PRODUCT}-${VERSIONSTRING}

CDROM_LABEL   =	Splitter ${VERSIONSTRING}

ifeq (${REPLYTO},)
	REPLYTO=${USER}@`hostname -f`
endif

PYTHON=`./python-test`

PREFIX = /usr
BINDIR = ${PREFIX}/bin
LIBDIR = ${PREFIX}/lib/splitter
MANDIR = ${PREFIX}/share/man/man8


BIN =	splitter

LIBS =	config.py \
	archive_list.py \
	utils.py

MAN = 	splitter.8


# stuff that should be handled via a site-config in /etc.  these are python
# constructs.
SIZE_LIMIT = 2**31
INDEX_FILE = "index.db"
INDEX_FILE_TTL = 3600
NODE_LIST = ['/scrap', '/home']


all: ${BIN} ${LIBS} #${MAN}.gz

${BIN}: template-${BIN} ${MAKEFILE}
	@echo "LIBDIR: ${LIBDIR}"
	@echo "PYTHON: ${PYTHON}"
	sed "s|__LIBDIR__|${LIBDIR}|" template-${BIN} > ${BIN}
	sed -i "s|__PYTHON_INTERPRETER__|${PYTHON}|" ${BIN}
	chmod 755 ${BIN}

config.py: template-config.py ${MAKEFILE}
	@echo "VERSION: ${VERSION}"
	@echo "DEVDATE: ${DEVDATE}"
	@echo "VERSIONSTRING: ${VERSIONSTRING}"
	@echo "SIZE_LIMIT: ${SIZE_LIMIT}"
	@echo "LIBDIR: ${LIBDIR}"
	@echo "INDEX_FILE: ${INDEX_FILE}"
	@echo "INDEX_FILE_TTL: ${INDEX_FILE_TTL}"
	@echo "NODE_LIST: ${NODE_LIST}"
	sed "s|__VERSION__|${VERSIONSTRING}|" template-config.py > config.py
	sed -i "s|__SIZE_LIMIT__|${SIZE_LIMIT}|" config.py
	sed -i "s|__LIBDIR__|${LIBDIR}|" config.py
	sed -i "s|__INDEX_FILE__|${INDEX_FILE}|" config.py
	sed -i "s|__INDEX_FILE_TTL__|${INDEX_FILE_TTL}|" config.py
	sed -i "s|__NODE_LIST__|${NODE_LIST}|" config.py

${MAN}.gz: template-${MAN}
	sed "s|FILL_ME_IN_CONFIG|${LIBDIR}/config.py|" template-${MAN} > ${MAN}
	gzip -f ${MAN}

install: ${BIN} ${LIBS} ${MAN}.gz
	mkdir -p ${PREFIX}
	mkdir -p ${BINDIR}
	mkdir -p ${LIBDIR}
	mkdir -p ${MANDIR}
	install -D ${BIN} ${BINDIR}/${BIN}
	cp ${LIBS} ${LIBDIR}
	cp ${MAN}.gz ${MANDIR}

dist: dist-bzip2

dist-bzip2: distclean
	@echo "DISTNAME: ${DISTNAME}"
	mkdir ${DISTNAME}
	tar -psc --exclude CVS --exclude ${DISTNAME} . | tar -C ${DISTNAME} -psx
	tar jcf ${DISTNAME}.tar.bz2 ${DISTNAME}
	rm -rf ${DISTNAME}

dist-srp: dist-bzip2
	mkdir t
	sed "s|__DISTNAME__|${DISTNAME}|" SRP_files/template-NOTES-2 > t/NOTES-2
	cp -p ${DISTNAME}.tar.bz2 t/
	cp -a SRP_files/* t/
	tar -C t -cf ${DISTNAME}-${PACKAGEREV}.srp --exclude CVS --exclude template-NOTES-2 .
	rm -rf t

# use this to specify path to srp, if need be
SRP = srp

dist-brp: dist-srp
	SRP_ROOT_PREFIX=${PWD}/t ${SRP} -F
	REPLYTO=${REPLYTO} SRP_ROOT_PREFIX=${PWD}/t ${SRP} -b ${DISTNAME}-${PACKAGEREV}.srp && rm -rf t

uninstall:
	rm -f ${BINDIR}/${BIN}
	rm -rf ${LIBDIR}
	rm -f ${MANDIR}/${MAN}.gz

clean:
	rm -f ${BIN} config.py ${MAN}.gz
	rm -f *.pyc *~
	rm -f *.tar.bz2 *.srp *.brp
	rm -rf t

distclean: clean
