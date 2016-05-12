

class MessageIDs(object):
    SSH_MSG_DISCONNECT = 1                  # [SSH-TRANS]
    SSH_MSG_IGNORE = 2                      # [SSH-TRANS]
    SSH_MSG_UNIMPLEMENTED = 3               # [SSH-TRANS]
    SSH_MSG_DEBUG = 4                       # [SSH-TRANS]
    SSH_MSG_SERVICE_REQUEST = 5             # [SSH-TRANS]
    SSH_MSG_SERVICE_ACCEPT = 6              # [SSH-TRANS]
    SSH_MSG_KEXINIT = 20                    # [SSH-TRANS]
    SSH_MSG_NEWKEYS = 21                    # [SSH-TRANS]
    SSH_MSG_USERAUTH_REQUEST = 50           # [SSH-USERAUTH]
    SSH_MSG_USERAUTH_FAILURE = 51           # [SSH-USERAUTH]
    SSH_MSG_USERAUTH_SUCCESS = 52           # [SSH-USERAUTH]
    SSH_MSG_USERAUTH_BANNER = 53            # [SSH-USERAUTH]
    SSH_MSG_GLOBAL_REQUEST = 80             # [SSH-CONNECT]
    SSH_MSG_REQUEST_SUCCESS = 81            # [SSH-CONNECT]
    SSH_MSG_REQUEST_FAILURE = 82            # [SSH-CONNECT]
    SSH_MSG_CHANNEL_OPEN = 90               # [SSH-CONNECT]
    SSH_MSG_CHANNEL_OPEN_CONFIRMATION = 91  # [SSH-CONNECT]
    SSH_MSG_CHANNEL_OPEN_FAILURE = 92       # [SSH-CONNECT]
    SSH_MSG_CHANNEL_WINDOW_ADJUST = 93      # [SSH-CONNECT]
    SSH_MSG_CHANNEL_DATA = 94               # [SSH-CONNECT]
    SSH_MSG_CHANNEL_EXTENDED_DATA = 95      # [SSH-CONNECT]
    SSH_MSG_CHANNEL_EOF = 96                # [SSH-CONNECT]
    SSH_MSG_CHANNEL_CLOSE = 97              # [SSH-CONNECT]
    SSH_MSG_CHANNEL_REQUEST = 98            # [SSH-CONNECT]
    SSH_MSG_CHANNEL_SUCCESS = 99            # [SSH-CONNECT]
    SSH_MSG_CHANNEL_FAILURE = 100           # [SSH-CONNECT]


class MessageDisconnect(object):
    SSH_DISCONNECT_HOST_NOT_ALLOWED_TO_CONNECT = 1
    SSH_DISCONNECT_PROTOCOL_ERROR = 2
    SSH_DISCONNECT_KEY_EXCHANGE_FAILED = 3
    SSH_DISCONNECT_RESERVED = 4
    SSH_DISCONNECT_MAC_ERROR = 5
    SSH_DISCONNECT_COMPRESSION_ERROR = 6
    SSH_DISCONNECT_SERVICE_NOT_AVAILABLE = 7
    SSH_DISCONNECT_PROTOCOL_VERSION_NOT_SUPPORTED = 8
    SSH_DISCONNECT_HOST_KEY_NOT_VERIFIABLE = 9
    SSH_DISCONNECT_CONNECTION_LOST = 10
    SSH_DISCONNECT_BY_APPLICATION = 11
    SSH_DISCONNECT_TOO_MANY_CONNECTIONS = 12
    SSH_DISCONNECT_AUTH_CANCELLED_BY_USER = 13
    SSH_DISCONNECT_NO_MORE_AUTH_METHODS_AVAILABLE = 14
    SSH_DISCONNECT_ILLEGAL_USER_NAME = 15


class ChannelOpenFailure(object):
    SSH_OPEN_ADMINISTRATIVELY_PROHIBITED = 1
    SSH_OPEN_CONNECT_FAILED = 2
    SSH_OPEN_UNKNOWN_CHANNEL_TYPE = 3
    SSH_OPEN_RESOURCE_SHORTAGE = 4


class DataTypeCode(object):
    SSH_EXTENDED_DATA_STDERR = 1


class TerminalModes(object):
    TTY_OP_END = 0       # Indicates end of options.
    VINTR = 1            # Interrupt character; 255 if none.  Similarly
    VQUIT = 2            # The quit character (sends SIGQUIT signal on
    VERASE = 3           # Erase the character to left of the cursor.
    VKILL = 4            # Kill the current input line.
    VEOF = 5             # End-of-file character (sends EOF from the
    VEOL = 6             # End-of-line character in addition to
    VEOL2 = 7            # Additional end-of-line character.
    VSTART = 8           # Continues paused output (normally
    VSTOP = 9            # Pauses output (normally control-S).
    VSUSP = 10           # Suspends the current program.
    VDSUSP = 11          # Another suspend character.
    VREPRINT = 12        # Reprints the current input line.
    VWERASE = 13         # Erases a word left of cursor.
    VLNEXT = 14          # Enter the next character typed literally,
    VFLUSH = 15          # Character to flush output.
    VSWTCH = 16          # Switch to a different shell layer.
    VSTATUS = 17         # Prints system status line (load, command,
    VDISCARD = 18        # Toggles the flushing of terminal output.
    IGNPAR = 30          # The ignore parity flag.  The parameter
    PARMRK = 31          # Mark parity and framing errors.
    INPCK = 32           # Enable checking of parity errors.
    ISTRIP = 33          # Strip 8th bit off characters.
    INLCR = 34           # Map NL into CR on input.
    IGNCR = 35           # Ignore CR on input.
    ICRNL = 36           # Map CR to NL on input.
    IUCLC = 37           # Translate uppercase characters to
    IXON = 38            # Enable output flow control.
    IXANY = 39           # Any char will restart after stop.
    IXOFF = 40           # Enable input flow control.
    IMAXBEL = 41         # Ring bell on input queue full.
    ISIG = 50            # Enable signals INTR, QUIT, [D]SUSP.
    ICANON = 51          # Canonicalize input lines.
    XCASE = 52           # Enable input and output of uppercase
    ECHO = 53            # Enable echoing.
    ECHOE = 54           # Visually erase chars.
    ECHOK = 55           # Kill character discards current line.
    ECHONL = 56          # Echo NL even if ECHO is off.
    NOFLSH = 57          # Don't flush after interrupt.
    TOSTOP = 58          # Stop background jobs from output.
    IEXTEN = 59          # Enable extensions.
    ECHOCTL = 60         # Echo control characters as ^(Char).
    ECHOKE = 61          # Visual erase for line kill.
    PENDIN = 62          # Retype pending input.
    OPOST = 70           # Enable output processing.
    OLCUC = 71           # Convert lowercase to uppercase.
    ONLCR = 72           # Map NL to CR-NL.
    OCRNL = 73           # Translate carriage return to newline
    ONOCR = 74           # Translate newline to carriage
    ONLRET = 75          # Newline performs a carriage return
    CS7 = 90             # 7 bit mode.
    CS8 = 91             # 8 bit mode.
    PARENB = 92          # Parity enable.
    PARODD = 93          # Odd parity, else even.
    TTY_OP_ISPEED = 128  # Specifies the input baud rate in
    TTY_OP_OSPEED = 129  # Specifies the output baud rate in


class ServiceNames(object):
    SSH_USERAUTH = b"ssh-userauth"      # [SSH-USERAUTH]
    SSH_CONNECTION = b"ssh-connection"  # [SSH-CONNECT]


class MethodNames(object):
    PUBLICKEY = b"publickey"  # [SSH-USERAUTH, Section 7]
    PASSWORD = b"password"    # [SSH-USERAUTH, Section 8]
    HOSTBASED = b"hostbased"  # [SSH-USERAUTH, Section 9]
    NONE = b"none"            # [SSH-USERAUTH, Section 5.2]


class ChannelTypes(object):
    SESSION = b"session"                  # [SSH-CONNECT, Section 6.1]
    X11 = b"x11"                          # [SSH-CONNECT, Section 6.3.2]
    FORWARDED_TCPIP = b"forwarded-tcpip"  # [SSH-CONNECT, Section 7.2]
    DIRECT_TCPIP = b"direct-tcpip"        # [SSH-CONNECT, Section 7.2]


class GlobalRequestNames(object):
    # [SSH-CONNECT, Section 7.1]
    TCPIP_FORWARD = b"tcpip-forward"
    # [SSH-CONNECT, Section 7.1]
    CANCEL_TCPIP_FORWARD = b"cancel-tcpip-forward"


class ChannelRequestNames(object):
    PTY_REQ = b"pty-req"             # [SSH-CONNECT, Section 6.2]
    X11_REQ = b"x11-req"             # [SSH-CONNECT, Section 6.3.1]
    ENV = b"env"                     # [SSH-CONNECT, Section 6.4]
    SHELL = b"shell"                 # [SSH-CONNECT, Section 6.5]
    EXEC = b"exec"                   # [SSH-CONNECT, Section 6.5]
    SUBSYSTEM = b"subsystem"         # [SSH-CONNECT, Section 6.5]
    WINDOW_CHANGE = b"window-change"  # [SSH-CONNECT, Section 6.7]
    XON_XOFF = b"xon-xoff"           # [SSH-CONNECT, Section 6.8]
    SIGNAL = b"signal"               # [SSH-CONNECT, Section 6.9]
    EXIT_STATUS = b"exit-status"     # [SSH-CONNECT, Section 6.10]
    EXIT_SIGNAL = b"exit-signal"     # [SSH-CONNECT, Section 6.10]


class SignalNames(object):
    ABRT = b"ABRT"  # [SSH-CONNECT]
    ALRM = b"ALRM"  # [SSH-CONNECT]
    FPE = b"FPE"    # [SSH-CONNECT]
    HUP = b"HUP"    # [SSH-CONNECT]
    ILL = b"ILL"    # [SSH-CONNECT]
    INT = b"INT"    # [SSH-CONNECT]
    KILL = b"KILL"  # [SSH-CONNECT]
    PIPE = b"PIPE"  # [SSH-CONNECT]
    QUIT = b"QUIT"  # [SSH-CONNECT]
    SEGV = b"SEGV"  # [SSH-CONNECT]
    TERM = b"TERM"  # [SSH-CONNECT]
    USR1 = b"USR1"  # [SSH-CONNECT]
    USR2 = b"USR2"  # [SSH-CONNECT]


class KeyExchangeMethods(object):
    # [SSH-TRANS, Section 8.1]
    DIFFIE_HELLMAN_GROUP1_SHA1 = b"diffie-hellman-group1-sha1"
    # [SSH-TRANS, Section 8.2]
    DIFFIE_HELLMAN_GROUP14_SHA1 = b"diffie-hellman-group14-sha1"


class EncryptionAlgorithmName(object):
    THREE_DES_CBC = b"3des-cbc"         # [SSH-TRANS, Section 6.3]
    BLOWFISH_CBC = b"blowfish-cbc"      # [SSH-TRANS, Section 6.3]
    TWOFISH256_CBC = b"twofish256-cbc"  # [SSH-TRANS, Section 6.3]
    TWOFISH_CBC = b"twofish-cbc"        # [SSH-TRANS, Section 6.3]
    TWOFISH192_CBC = b"twofish192-cbc"  # [SSH-TRANS, Section 6.3]
    TWOFISH128_CBC = b"twofish128-cbc"  # [SSH-TRANS, Section 6.3]
    AES256_CBC = b"aes256-cbc"          # [SSH-TRANS, Section 6.3]
    AES192_CBC = b"aes192-cbc"          # [SSH-TRANS, Section 6.3]
    AES128_CBC = b"aes128-cbc"          # [SSH-TRANS, Section 6.3]
    SERPENT256_CBC = b"serpent256-cbc"  # [SSH-TRANS, Section 6.3]
    SERPENT192_CBC = b"serpent192-cbc"  # [SSH-TRANS, Section 6.3]
    SERPENT128_CBC = b"serpent128-cbc"  # [SSH-TRANS, Section 6.3]
    ARCFOUR = b"arcfour"                # [SSH-TRANS, Section 6.3]
    IDEA_CBC = b"idea-cbc"              # [SSH-TRANS, Section 6.3]
    CAST128_CBC = b"cast128-cbc"        # [SSH-TRANS, Section 6.3]
    NONE = b"none"                      # [SSH-TRANS, Section 6.3]
    DES_CBC = b"des-cbc"                # [FIPS-46-3] HISTORIC; See


class MACAlgorithmNames(object):
    HMAC_SHA1 = b"hmac-sha1"        # [SSH-TRANS, Section 6.4]
    HMAC_SHA1_96 = b"hmac-sha1-96"  # [SSH-TRANS, Section 6.4]
    HMAC_MD5 = b"hmac-md5"          # [SSH-TRANS, Section 6.4]
    HMAC_MD5_96 = b"hmac-md5-96"    # [SSH-TRANS, Section 6.4]
    NONE = b"none"                  # [SSH-TRANS, Section 6.4]


class PublicKeyAlgorithmNames(object):
    SSH_DSS = b"ssh-dss"            # [SSH-TRANS, Section 6.6]
    SSH_RSA = b"ssh-rsa"            # [SSH-TRANS, Section 6.6]
    PGP_SIGN_RSA = b"pgp-sign-rsa"  # [SSH-TRANS, Section 6.6]
    PGP_SIGN_DSS = b"pgp-sign-dss"  # [SSH-TRANS, Section 6.6]


class CompressionAlgorithmNames(object):
    NONE = b"none"  # [SSH-TRANS, Section 6.2]
    ZLIB = b"zlib"  # [SSH-TRANS, Section 6.2]
