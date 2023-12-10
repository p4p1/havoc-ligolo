# havoc-ligolo
A Havoc UI tool to pivot onto a machine using ligolo-ng

# Usage
To connect to ligolo on the agent you first need to setup. In this example I have
my havoc client on 192.168.8.0/24 and a windows machine that I use for the victim on
10.0.2.0/24 The windows client is able to ping 10.0.2.2 but the havoc linux machine
can't as shown bellow:

![image](https://github.com/p4p1/havoc-ligolo/assets/19672114/1ca8393e-2529-4d3b-9d21-914da95c77f8)
![image](https://github.com/p4p1/havoc-ligolo/assets/19672114/fa7992e2-a521-4e84-a196-ff1da070825b)

## Setup the client server

You first need to setup the server to listen on the correct ip address and port.
In my example the windows machine does not have any firewall but if you need to listen
on a protected port you can activate a "sudo" mode for the ligolo server inside of it's
settings. To setup the server open the settings in Ligolo > Settings:

![image](https://github.com/p4p1/havoc-ligolo/assets/19672114/bcda118e-3bd3-46ca-85f0-49050a586bff)

## Adding ranges

From there we then click on save and need to add the cidr of the client by using
the "Add IP range" pop-up inside of Ligolo > Add IP range:

![image](https://github.com/p4p1/havoc-ligolo/assets/19672114/eefe1325-b89d-4f63-a7ac-13696e9f7060)

> Note that if the server is running adding ranges will automatically be added to
> the routes of the client's machine

## Starting the server

We can then start the server by selecting Ligolo > Start server option which will
prompt you multiple times for you sudo password to create the routes and the interfaces

![image](https://github.com/p4p1/havoc-ligolo/assets/19672114/3a5f8d97-5d1c-446e-ba12-a2d019bec9aa)

After filling in your root password a few times for all of the commands you will then be
prompted with the command to access your ligolo server through a tmux session:

![image](https://github.com/p4p1/havoc-ligolo/assets/19672114/9cdc566a-a799-4c74-81bc-b84132c46232)

From there you can manage your ligolo server:

![image](https://github.com/p4p1/havoc-ligolo/assets/19672114/bccfbfb4-4f77-40dd-b904-1b728843153d)
