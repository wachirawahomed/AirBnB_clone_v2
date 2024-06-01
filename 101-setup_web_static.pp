# Define Nginx class
class nginx {
  package { 'nginx':
    ensure => installed,
  }
  
  file { '/etc/nginx/sites-available/default':
    ensure  => file,
    content => template('nginx/default.erb'),
    notify  => Service['nginx'],
  }
  
  service { 'nginx':
    ensure    => running,
    enable    => true,
    subscribe => File['/etc/nginx/sites-available/default'],
  }
}

# Define web_static class
class web_static {
  # Create directories
  file { ['/data/web_static/releases/test', '/data/web_static/shared']:
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }
  
  # Create a fake HTML file
  file { '/data/web_static/releases/test/index.html':
    ensure  => file,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644',
    content => "<html>\n<head>\n</head>\n<body>\n  Holberton School\n</body>\n</html>\n",
  }
  
  # Create symbolic link
  file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test',
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }
}

# Include both classes
include nginx
include web_static
