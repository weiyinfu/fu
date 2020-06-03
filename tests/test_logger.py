from fu import log

log.root.info('haha')
log.root.debug('baga')
x = log.getFileLogger('haha', 'haha.txt')
x.info('haha')
x.debug('haha')
