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

resource "digitalocean_volume" "vol" {
  region                  = "sfo3"
  name                    = "vol"
  size                    = 1024
  initial_filesystem_type = "ext4"

}

resource "digitalocean_droplet" "server" {
  image     = "debian-11-x64"
  name      = "volume-sfo3-01"
  region    = "sfo3"
  size      = "s-8vcpu-16gb"
  ssh_keys  = [for key in data.digitalocean_ssh_keys.keys.ssh_keys : key.fingerprint]
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

  provisioner "file" {
    source      = "do_token.txt"
    destination = "/root/do_token.txt"
  }
}

resource "digitalocean_volume_attachment" "vol_to_server" {
  droplet_id = digitalocean_droplet.server.id
  volume_id  = digitalocean_droplet.vol.id
}

output "server_ip" {
  value = resource.digitalocean_droplet.server.ipv4_address
}

