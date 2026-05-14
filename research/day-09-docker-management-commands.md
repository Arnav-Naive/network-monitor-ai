# Docker Management Guide for Beginners

## What is Docker?

Think of Docker like a **mini computer inside your computer**. Instead of installing programs directly on your machine, you run them in isolated "containers" - like running a program in its own separate room.

**Your case:** Your SNMP virtual switch runs inside a Docker container called `virtual-switch`.

---

## Understanding Through Your Monitor Script

You already know how to manage Python scripts. Docker is similar:

| Action | Python Script | Docker Container |
|--------|--------------|------------------|
| Start | `python monitor.py` | `docker start virtual-switch` |
| Stop | Press `Ctrl+C` | `docker stop virtual-switch` |
| Check output | See terminal window | `docker logs virtual-switch` |
| Restart | Run script again | `docker start virtual-switch` |

---

## Quick Reference Commands

### Check What's Running

```bash
docker ps
```

**What it does:** Shows all running containers (like Task Manager for Docker)

---

### Start Your Container

```bash
docker start virtual-switch
```

**What it does:** Starts the container. Like running your Python script.  
**When to use:** After you've stopped it or after reboot.

---

### Stop Your Container

```bash
docker stop virtual-switch
```

**What it does:** Stops the container gracefully (like pressing `Ctrl+C`).  
**Note:** Container still exists, your files inside are safe. You can start it again.

---

### View Logs (See What Happened)

```bash
docker logs virtual-switch
```

**What it does:** Shows all output from the SNMP daemon - errors, warnings, messages.  
**When to use:** When something isn't working and you need to debug.

---

### Remove Container Completely

```bash
docker stop virtual-switch
docker rm virtual-switch
```

**What it does:** Deletes the container completely.  
**Warning:** Container is gone. You'd need to run `docker run` again to recreate it.

---

## When to Use What

| Situation | Command |
|-----------|---------|
| **Check if running** | `docker ps` |
| **Pause for now** | `docker stop virtual-switch` |
| **Resume later** | `docker start virtual-switch` |
| **Something's broken** | `docker logs virtual-switch` |
| **Changed config files** | Rebuild (see below) |
| **Done with project** | `docker stop virtual-switch`<br>`docker rm virtual-switch` |

---

## Rebuilding the Container

If you changed the Dockerfile or configuration files, you need to rebuild:

```bash
# Step 1: Stop the container
docker stop virtual-switch

# Step 2: Remove the old container
docker rm virtual-switch

# Step 3: Build the new image
docker build -t snmp-switch .

# Step 4: Create and start new container
docker run -d -p 161:161/udp --name virtual-switch snmp-switch
```

---

## Common Scenarios

### Scenario 1: Computer Restarted
**Problem:** Container stopped after restart.  
**Solution:**
```bash
docker start virtual-switch
```

---

### Scenario 2: Not Sure If It's Running
**Check:**
```bash
docker ps
```
**Look for:** A line with `virtual-switch` in it. If you see it, it's running.

---

### Scenario 3: Something's Not Working
**Debug:**
```bash
docker logs virtual-switch
```
Look at the end of the logs for error messages.

---

### Scenario 4: Want to Start Fresh
**Clean slate:**
```bash
docker stop virtual-switch
docker rm virtual-switch
# Then rebuild and run again
```

---

## Important Notes

1. **Container vs Image:** 
   - **Image** = The blueprint (like your Python script file)
   - **Container** = The running instance (like when you run the script)

2. **Data Safety:** 
   - Stopping a container is safe - data stays
   - Removing a container deletes it - rebuild needed

3. **Port 161:** 
   - Your container uses UDP port 161 for SNMP
   - Make sure nothing else is using this port

---

## Need Help?

Run `docker --help` or `docker COMMAND --help` for more info on any command.