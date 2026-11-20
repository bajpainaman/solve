import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.rmi.server.RMISocketFactory;

/**
 * A Java agent that lets TLC start in a shell that forbids listening sockets.
 *
 * TLC exports its fingerprint set as an RMI object, and the export opens a
 * listening socket. Only distributed TLC connects to that socket. This agent
 * gives RMI a server socket that is never bound and whose accept() never
 * returns, so a check on one machine runs unchanged.
 *
 * fv-install tla compiles this file into no-rmi-listen.jar, and fv-tlc adds it
 * with -javaagent only after TLC failed with "Listen failed".
 */
public final class NoRmiListen {
    public static void premain(String arguments) throws IOException {
        RMISocketFactory.setSocketFactory(new RMISocketFactory() {
            @Override
            public Socket createSocket(String host, int port) throws IOException {
                throw new IOException("RMI client sockets are switched off by the fv-toolkit socket agent");
            }

            @Override
            public ServerSocket createServerSocket(int port) throws IOException {
                return new ServerSocket() {
                    @Override
                    public int getLocalPort() {
                        return 1;
                    }

                    @Override
                    public Socket accept() throws IOException {
                        try {
                            Thread.sleep(Long.MAX_VALUE);
                        } catch (InterruptedException interrupted) {
                            Thread.currentThread().interrupt();
                        }
                        throw new IOException("closed");
                    }
                };
            }
        });
    }
}
