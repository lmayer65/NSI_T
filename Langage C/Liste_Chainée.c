#include <stdio.h>
#include <stdlib.h>



struct Node {
	int val;     		// Valeur associ�e
	struct Node *next;  // Pointe sur le noeud suivant	
};


struct Node * init(int);  		// Initialise la cha�ne
void add(struct Node *, int);   // Ajout d'un �l�ment
void del(struct Node *);        // Supprime la cha�ne
void print(struct Node *);      // Affiche la liste cha�n�e


int main()
{
	// D�claration d'une liste cha�n�e
	struct Node *lst = NULL;
	
	lst = init(1); add(lst, 2); add(lst, 3);
	
	// Attendu : 1,2,3
	print(lst);
	
	// Suppression de la liste
	del(lst);
	lst = NULL;
	
	return 0;	
}



struct Node *  init(int n_val) {
	// Attention � indiquer la taille de la structure
	struct Node *c_node = (struct Node *)malloc(sizeof(struct Node));
	
	// et non de son pointeur
	c_node->next = NULL; // Pas de suivant
	c_node->val = n_val;
	
	return c_node;	
}


void add(struct Node *c_node, int n_val) {
	// Si la cha�ne n'est pas valide
	if (c_node == NULL) {
		printf("Chaine vide ou incorrecte");
		return; // On pourrait quitter le programme
	}
	
	// Constrution du noeud suivant
	struct Node *n_node = NULL;
	n_node = (struct Node *)malloc(sizeof(struct Node));
	n_node->next = NULL; // Il est le dernier maillon
	n_node->val = n_val;
	
	// Acc�s au dernier �l�ment de la liste
	// pour ajouter le nouvel �l�ment en fin de liste
	while (c_node->next != NULL)
		// R�cup�ration du noeud suivant
		c_node = c_node->next;
		
	// Le noeud pr�c�dent a d�sormais un suivant
	c_node->next = n_node;	
}


void del(struct Node *c_node) {
	
	struct Node *n_node = NULL;
	
	// Tant que la cha�ne n'est pas vide
	while (c_node != NULL) {
		// R�cup�ration du noeud suivant
		n_node = c_node->next;
		// D�sallouement de c_node
		free(c_node);
		// c_node devient le noeud suivant
		c_node = n_node;
	}
}


void print(struct Node *c_node) {
	if (c_node == NULL) {
		printf("Cha�ne vide");
		return;
		}
		
	// Tant que la cha�ne n'est pas vide
	while (c_node != NULL) {
		// On affiche la valeur du noeud
		printf("%i \t", c_node->val);
		// c_node devient le noeud suivant
		c_node = c_node->next;
	}
	
	printf("\n");
}













