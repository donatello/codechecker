from datetime import datetime
class Logger:

    RUNTIME, DEBUG = range( 2 )

    def __init__( self, module_name, logfile ):
        self.logfile = logfile
        self.module_name = module_name

    def log( self, message, log_type ):
        header = { 0 : '[runtime]',
                   1 : '[debug]' }
        f = file( self.logfile, "a" )
        f.write( header[log_type] + ' ' +
                message + ' ' +
                '[' + str( datetime.now().ctime() ) + '] ' +
                '[' + self.module_name + '] '"\n" )
        f.close()

if __name__ == "__main__":
    l = Logger( __file__, "/tmp/testinglog" ).log
    l( "yhello world", Logger.DEBUG )
