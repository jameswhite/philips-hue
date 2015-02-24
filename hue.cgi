#!/usr/bin/env perl
require LWP::UserAgent;
require Data::Dumper;
require JSON;
require CGI;

my $ua = LWP::UserAgent->new;

$ua->timeout(10);
$ua->env_proxy;

# This is a wrapping value between 0 and 65535. Both 0 and 65535 are red, 25500 is green and 46920 is blue.
my $color = {
              'red'       => hex("0x0000"),
              'orange'    => hex("0x1800"),
              'yellow'    => hex("0x4000"),
              'green'     => hex("0x639C"),
              'cyan'      => hex("0x9000"),
              'blue'      => hex("0xB748"),
              'indigo'    => hex("0xC000"),
              'lavender'  => hex("0xD000"),
              'pink'      => hex("0xE000"),
              'gold'      => hex("0x1D3C"),
            };

my $lights = {
               'closet'    => [ 1 ],
               'bedroom'    => [ 2 ],
               'livingroom' => [ 3 ],
               'windows'    => [ 4, 5 ],
               'entry'      => [ 6, 7 ],
               'bath'       => [ 11, 8 , 10 ],
               'laundry'    => [ 9 ],
             };

sub get ($){
    my $url = shift @_;
    my $response = $ua->get($url);
    if ($response->is_success) {
        print $response->decoded_content;  # or whatever
    }else{
        die $response->status_line;
    };
    print "\n";
}

sub put ($$){
    my $uri = shift;
    my $data = shift;
    my $json = JSON->new->allow_nonref;

    my $req = HTTP::Request->new( 'PUT', $uri );
    $req->header( 'Content-Type' => 'application/json' );
    $req->content( $json->encode($data) );
    my $lwp = LWP::UserAgent->new;
    my $response = $lwp->request( $req );
    print Data::Dumper->Dump([$response->{'_content'}]);
}

sub color($$){
   my $room = shift;
   my $color = shift;
   if($room eq "all"){
     put("http://philips-hue/api/$ENV{'HUE_USER'}/groups/0/action", { 'on' => $JSON::true, 'sat' => 255, 'bri' => 255, 'hue' => $color });
   }else{
     foreach $light (@{$lights->{$room}}){
       put("http://philips-hue/api/$ENV{'HUE_USER'}/lights/$light/state", { 'on' => $JSON::true, 'sat' => 255, 'bri' => 255, 'hue' => $color });
     }
   }
}

sub white($){
   my $room = shift;
   if($room eq "all"){
     put("http://philips-hue/api/$ENV{'HUE_USER'}/groups/0/action", { 'on' => $JSON::true, 'sat' => 0, 'bri' => 255, 'hue' => $color });
   }else{
     foreach $light (@{$lights->{$room}}){
       put("http://philips-hue/api/$ENV{'HUE_USER'}/lights/$light/state", { 'on' => $JSON::true, 'sat' => 0, 'bri' => 255, 'hue' => $color });
     }
   }
}

sub state($){
    my $room = shift;
    foreach my $light (@{ $lights->{ $room } }){
      get("http://philips-hue/api/$ENV{'HUE_USER'}/lights/$light/state")
    }
}

sub all_color($){
   my $color = shift;
   color('all', $color);
}

sub all_white{
   put("http://philips-hue/api/$ENV{'HUE_USER'}/groups/0/action", { 'on' => $JSON::true, 'sat' => 0, 'bri' => 255, 'hue' => $color->{'blue'} });
}

sub all_off{
   put("http://philips-hue/api/$ENV{'HUE_USER'}/groups/0/action", { 'on' => $JSON::false, 'sat' => 0, 'bri' => 255, 'hue' => $color->{'blue'} });
}

# # foreach my $count ( 1..3 ){ all_color($red); sleep(1); all_white(); sleep(1); all_color($blue); sleep(1); } sleep(1); }
# foreach my $room ('closet', 'bedroom', 'livingroom', 'windows', 'entry', 'bath', 'laundry'){
#     foreach my $color ($red, $orange, $yellow, $green, $cyan, $blue, $indigo, $lavender, $pink){
#         color($room,$color);
#         sleep(1);
#         all_white();
#         sleep(1);
#     }
# }

my $q = CGI->new;
$ENV{'HUE_USER'}=$q->param('user');
print "Content-type: text/plain\n\n";

if($q->param('action') eq 'all_off'){
    all_off();
}elsif($q->param('action') eq 'all_on'){
    all_white();
}elsif($q->param('action') eq 'on'){
    white( $q->param('room') );
}else{
    color( $q->param('room'), $color->{$q->param('color')} );
}
