
class MailConverter:
    regex = '[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'

    def to_python(self, value):
        return string(value) # FIXME - Erro em string()

    def to_url(self, value):
        return '%04d' % value
