terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = file("do_token.txt")
}

data "digitalocean_ssh_keys" "keys" {
  sort {
    key       = "name"
    direction = "asc"
  }
}

resource "digitalocean_droplet" "server" {
  image     = "debian-11-x64"
  name      = "dhdb-quest"
  region    = "sfo3"
  size      = "s-8vcpu-16gb"
  ssh_keys  = [ for key in data.digitalocean_ssh_keys.keys.ssh_keys: key.fingerprint ]
  user_data = file("provision.sh")

  connection {
    host        = self.ipv4_address
    user        = "root"
    type        = "ssh"
    timeout     = "2m"
    private_key = file("~/.ssh/id_ed25519")
  }

  provisioner "file" {
    source      = "~/.dolt"
    destination = "/root"
  }
}

resource "digitalocean_droplet" "devserver" {
  image     = "debian-11-x64"
  name      = "dhdb-quest-sqlserver-dev"
  region    = "sfo3"
  size      = "s-8vcpu-16gb"
  ssh_keys  = [ for key in data.digitalocean_ssh_keys.keys.ssh_keys: key.fingerprint ]
  user_data = file("provision_sql_server.sh")

  connection {
    host        = self.ipv4_address
    user        = "root"
    type        = "ssh"
    timeout     = "2m"
    private_key = file("~/.ssh/id_ed25519")
  }

  provisioner "file" {
    source      = "~/.dolt"
    destination = "/root"
  }
}

output "server_ip" {
  value = resource.digitalocean_droplet.server.ipv4_address
}

output "dev_server_ip" {
  value = resource.digitalocean_droplet.devserver.ipv4_address
}

