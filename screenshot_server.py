from mcp.server.fastmcp import FastMCP, Image
import mss
import mss.tools
import io
import base64

# Create an MCP server
mcp = FastMCP("Screenshot Server")

@mcp.tool()
def take_screenshot() -> Image:
    """Takes a screenshot of the main screen and returns it as an Image."""
    with mss.mss() as sct:
        # Get information of monitor 1
        monitor = sct.monitors[1]

        # Grab the data
        sct_img = sct.grab(monitor)

        # Convert to PNG bytes
        png_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)

        # Return as an Image object which FastMCP expects
        return Image(data=png_bytes, format="png")

if __name__ == "__main__":
    mcp.run()
