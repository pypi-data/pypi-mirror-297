class LogRecord:
    class Level:
        I = 'INFO'
        W = 'WARN'
        E = 'ERROR'

    def __init__(self, level, source, message, tag_pairs):
        self.level = level
        self.source = source
        self.message = message
        tag_map = {}
        if tag_pairs:
            for i in range(0, len(tag_pairs), 2):
                tag_map[tag_pairs[i]] = tag_pairs[i + 1]
        self.tagMap = tag_map
