#include <stdio.h>
#include <stdlib.h>



struct Node {
	int val;     		// Valeur associée
	struct Node *next;  // Pointe sur le noeud suivant	
};


struct Node * init(int);  		// Initialise la chaîne
void add(struct Node *, int);   // Ajout d'un élément
void del(struct Node *);        // Supprime la chaîne
void print(struct Node *);      // Affiche la liste chaînée


int main()
{
	// Déclaration d'une liste chaînée
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
	// Attention à indiquer la taille de la structure
	struct Node *c_node = (struct Node *)malloc(sizeof(struct Node));
	
	// et non de son pointeur
	c_node->next = NULL; // Pas de suivant
	c_node->val = n_val;
	
	return c_node;	
}


void add(struct Node *c_node, int n_val) {
	// Si la chaîne n'est pas valide
	if (c_node == NULL) {
		printf("Chaine vide ou incorrecte");
		return; // On pourrait quitter le programme
	}
	
	// Constrution du noeud suivant
	struct Node *n_node = NULL;
	n_node = (struct Node *)malloc(sizeof(struct Node));
	n_node->next = NULL; // Il est le dernier maillon
	n_node->val = n_val;
	
	// Accès au dernier élément de la liste
	// pour ajouter le nouvel élément en fin de liste
	while (c_node->next != NULL)
		// Récupération du noeud suivant
		c_node = c_node->next;
		
	// Le noeud précédent a désormais un suivant
	c_node->next = n_node;	
}


void del(struct Node *c_node) {
	
	struct Node *n_node = NULL;
	
	// Tant que la chaîne n'est pas vide
	while (c_node != NULL) {
		// Récupération du noeud suivant
		n_node = c_node->next;
		// Désallouement de c_node
		free(c_node);
		// c_node devient le noeud suivant
		c_node = n_node;
	}
}


void print(struct Node *c_node) {
	if (c_node == NULL) {
		printf("Chaîne vide");
		return;
		}
		
	// Tant que la chaîne n'est pas vide
	while (c_node != NULL) {
		// On affiche la valeur du noeud
		printf("%i \t", c_node->val);
		// c_node devient le noeud suivant
		c_node = c_node->next;
	}
	
	printf("\n");
}













