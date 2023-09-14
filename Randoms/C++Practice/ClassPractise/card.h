class Card
{
    private:
        int ease;
        int dueDate;
        char faces[2][32];
    public:
        Card();

        Card(int theease, int theduedate, char thefaces);

        int getDueDate() const {return dueDate;}
};