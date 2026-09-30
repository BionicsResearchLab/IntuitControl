# IntuitCortex Backend

Communicates with the Cortex API using the WebSocket Secure Protocol (WSS).
1. Create a WebSocket Client
2. Connect to LocalHost
- Port: 6868
- Protocol: wss
3. Communicate with Cortex using the JSON-RPC 2.0 Protocl
- Call methods (w or w/o) parameters
- JSON-RPC 2.0 format
{
    "jsonrpc": "2.0",
    "method": "someMethod",
    "params": {},
    "id": 1
}