FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-server sudo tar && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd && ssh-keygen -A

RUN useradd -m -s /bin/bash n.fernando && \
    echo "n.fernando:N1ghtly_B4ckup_2024" | chpasswd

RUN echo "n.fernando ALL=(root) NOPASSWD: /usr/bin/tar" > /etc/sudoers.d/n-fernando && \
    chmod 440 /etc/sudoers.d/n-fernando && \
    visudo -c -f /etc/sudoers.d/n-fernando

RUN echo "PT{tar_chkpt_r00t_esc4l4t10n}" > /root/flag.txt && \
    chmod 600 /root/flag.txt && \
    chown root:root /root/flag.txt

RUN sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
