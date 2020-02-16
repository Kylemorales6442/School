
	
struct student{
	char *name;
	int id;
	int scores[5];
	double gpa;
};

struct course {
	char *name;
	int num;
	char *instructor;
};

int main() {
	struct student anky  = { "Ankunda Kiremire", 69420, {90, 92, 100, 99, 105}    , 3.5 };
	struct student timmy = { "Andrey Timofeyev", 1337 , {100, 120, 100, 140, 9001}, 6.0 };
	struct student gourd = { "Gene Gourd"      , 130  , {0, 0, 69, 0, 0}          , 1.9 };
	
	struct course wasteoftime = { "British History"    , 42069    , "Dr. Who Even Cares" };
	struct course coolstuff   = { "Systems Programming", 123456789, "timmy" };
	struct course easyA       = { "Data Structures"    , 11111111 , "Mr. A. F. Kay" };
}