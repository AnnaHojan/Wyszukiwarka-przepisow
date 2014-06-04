#!/usr/bin/perl

use XML::Simple;
use LWP::Simple;
use Data::Dumper;
use JSON;

use strict;
use warnings;


sub fix($) {
	my ($str) = @_;
	$str = defined $str ? $str : '';
	$str = '' if ref $str eq ref {};
	return lc($str);
}

sub fix_long($) {
	my ($str) = @_;
	$str = fix($str);
	$str =~ s/&nbsp/ /g;
	$str =~ s/\n/ /g;
	$str =~ s/\d//g;
	$str =~ s/\p{P}/ /g;
	$str =~ s/<[^>]*>//g;
	return $str;
}

die "Podaj zakres od i do" if $#ARGV < 1;
my ($od, $do) = @ARGV;

my $i = $od;

#my $json_hash = {};
my $json = JSON->new;

my @api_keys = (
	'dvxgq38c2yR4Cm35r7WN3XhpII8A7PLS',
	'dvxZTjv1008Q8PmW9K1H54M65Ob3V0nF',
	'dvxNGs1U4Gpj9ivFO8Lv9et8GDbaGQ22',
	'dvx35egIri60Tl4Gm1i9dat351OwWZ50',
	'dvxH3xqgevXiicPp7X4oARjLEiV8k9Vx',
	'dvxVvgjqTkgMd2C23RN9j0t84848z0Mu',
	'dvx9pSE9ssYp57JBmHkC4wX3NY52z48P',
	'dvxsu9muedipq9JTSOmazf06G2TaFpk6',
	'dvxbGgp47xZ8yaLFTV0t8kyt8AO0jlq1',
	'dvxg86650P4x2jtJj1ZDRP9h8Yg1wsox',
	'dvxAMZ6bcUUFIdw4wITA4HAImIX357Ki',
	'dvx00a6Kbk7b2mfwPOl8cb19d3b740aR',
);
my $api_keys_size = scalar @api_keys;
my $liczba_pobran = 0;
my $licznik_api_key = 0;

while ($i <= $do) {
	
	if ($liczba_pobran == 90) {
		$licznik_api_key++;
		print "Zmiana api_key na $licznik_api_key\n";
		$liczba_pobran = 0;
		if ($licznik_api_key == $api_keys_size) {
			$licznik_api_key = 0;
			my ($second, $minute, $hour, $dayOfMonth, $month, $yearOffset, $dayOfWeek, $dayOfYear, $daylightSavings) = localtime();
			print "Goin' to sleep at $hour:$minute\n";
			sleep(3720);
		}
		
	}
	my $data = get("http://api.bigoven.com/recipe/$i?api_key=". $api_keys[$licznik_api_key]);
	my $parser = new XML::Simple;
	my $dom = $parser->XMLin($data);
	$liczba_pobran++;

	if (defined $dom->{StatusCode} && defined $dom->{Message}) {
		print $dom->{Message} . "\n";
		if ($dom->{Message} eq 'Recipe not found.') {
			$i++;
			next;
		}
		$licznik_api_key++;
		print "Zmiana api_key na $licznik_api_key\n";
		$liczba_pobran = 0;
		if ($licznik_api_key == $api_keys_size) {
			$licznik_api_key = 0;
			my ($second, $minute, $hour, $dayOfMonth, $month, $yearOffset, $dayOfWeek, $dayOfYear, $daylightSavings) = localtime();
			print "Goin' to sleep at $hour:$minute\n";
			sleep(3720);
		}
		next;
	}
	

	if (defined $dom->{StatusCode} || !defined $dom->{Title} || !defined $dom->{RecipeID} || (!defined $dom->{Cuisine} && !defined $dom->{Category})) {
		print "Error dla id = $i"; print"\n";
		$i++;
		next;
	}
	
	my $Cuisine = fix($dom->{Cuisine});
	my $Category = fix($dom->{Category});
	
	my $TotalMinutes = fix($dom->{TotalMinutes});
	
	my $RecipeID = fix($dom->{RecipeID});
	my $Instructions = fix($dom->{Instructions});
	my $Title = fix($dom->{Title});
	my $PrimaryIngredient = fix($dom->{PrimaryIngredient});
	my $Subcategory = fix($dom->{Subcategory});
	
	my $tresc = "$Title $PrimaryIngredient $Instructions $Subcategory";

	if (ref $dom->{Ingredients}->{Ingredient} eq ref {}) {
		my $Name = fix($dom->{Ingredients}->{Ingredient}->{Name});
		my $PreparationNotes = fix($dom->{Ingredients}->{Ingredient}->{PreparationNotes});
		$tresc = "$tresc $Name $PreparationNotes"
	} else {
		for my $ingr (@{$dom->{Ingredients}->{Ingredient}}) {
			my $Name = fix($ingr->{Name});
			my $PreparationNotes = fix($ingr->{PreparationNotes});
			$tresc = "$tresc $Name $PreparationNotes"
		}
	}
	$tresc = fix_long($tresc);
	
	my @kategorie = ();
	push @kategorie, $Cuisine if $Cuisine ne '';
	push @kategorie, $Category if $Category ne '';
	
	my $elem = {id => $RecipeID, tresc => $tresc, kategorie => \@kategorie, czas => $TotalMinutes, tytul => $Title};
	#$json_hash->{$RecipeID} = $elem;
	
	
	my $filename = "$RecipeID-";
	for my $cat (@kategorie) {
		$filename .= "_$cat";
	}
	$filename .= $TotalMinutes ? "^$TotalMinutes" : "^0";
	$filename .= '.txt';
	
	open my $out1, ">", $filename or die("Could not open file. $!");
	print $out1 $tresc;
	close ($out1); 
	
	$i++;
}

#my $encoded_json = $json->encode($json_hash) . "\n";

#open (out2, '>json.txt');
#print out2 $encoded_json;
#close (out2);