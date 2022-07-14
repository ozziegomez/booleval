
Boolean Evaluator
#################

**booleval** es una *command line utility* que evalúa expresiones lógicas e imprime sus tablas de verdad.


Grammar
=======

.. code ::

	<eval> ::= ";"
	       |   "exit"
	       |   <prop>
	       |   <eval> <prop>
			
	<prop> ::= <term>
	       |   <prop>  "->"  <term>
	       |   <prop> "<->"  <term>
	       |   <prop> "<~>"  <term>

	<term> ::= <atom>
	       |   <term> "&" <atom>
	       |   <term> "|" <atom>
	       |   <term> "!" <atom>

	<atom> ::= <id>
	       | "~" <atom>
	       | "(" <prop> ")"
	       | "[" <prop> "]"
	       | "{" <prop> "}"

	<id> ::= [a-zA-Z]{1,1}



Conectores Lógicos
==================


La sig. tabla muestra los conectores lógicos y su equivalente implementados en :code:`booleval` (**Booleval**):

======================== ====== ========
Conector                 Lógica Booleval
======================== ====== ========
Negación                  ¬        ~
Conjunción                ˄       &
Disyunción                ˅       \|
`Disyunción Exclusiva`_   ⊻       <~>
Condicional               →      ->
Bicondicional             ↔      <->
`Negación Conjunta`_       ↓       !
======================== ====== ========

.. _`Disyunción Exclusiva`: https://es.wikipedia.org/wiki/Disyunci%C3%B3n_exclusiva
.. _`Negación Conjunta`: https://es.wikipedia.org/wiki/Disyunci%C3%B3n_opuesta

**Puntuadores**: como comenté anteriormente, cada expresión debe terminar con :code:`;`. También podemos utilizar :code:`()`, :code:`[]` y :code:`{}` como separadores.
Además, ``booleval`` reconoce los comentarios de una línea (como en **Python**), todo lo que esté luego del caracter :code:`#` hasta el salto de línea será ignorado. Los comentarios son (más) útiles para documentar las expresiones cuando las tengamos en un archivo.


Ejemplos
~~~~~~~~

Cada expresión lógica debe terminar en '``;``', esto hace posible que ``booleval`` pueda procesar varias de estas al mismo tiempo (separadas por ``;``). La siguiente expresión lógica :math:`(p\ \wedge\ q → r)` se la podemos pasar a ``booleval`` como: :code:`(p & q -> r);`. **Nota**: la precedencia y asociatividad de los conectores lógicos está programada en la utilidad, por lo que todas las siguientes expresiones son equivalentes: :math:`(p\ \wedge\ q) → r \equiv \{(p\ \wedge\ q) → r\}  \equiv p\ \wedge\ q → r`.

**Uso**

- **Arrancar el programa**

.. code :: 

	$ python -m booleval 

Luego de ejecutar el comando anterior, la utilidad nos responde mostrandonos el siguiente *prompt* '``>``' que nos señala que está lista para evaluar expresiones:

.. code ::

	$>

- **Corrida**. Nota que lo que aparece luego de :code:`;` es un comentario:

.. code ::

	$> ~(p & q) <-> (~p | ~q);  # De Morgan's Law

- **Salida**. 

La línea final de la tabla muestra si se trata de una *Tautología* (``tautology``), *Contradicción* (``contradiction``) o una *Contingencia* (``contingent``):

.. code ::

	p  q  (p&q)  ~(p&q)  ~p  ~q  (~p|~q)  ~(p&q)<->(~p|~q)
	======================================================
	V  V    V       F     F   F     F             V
	V  F    F       V     F   V     V             V
	F  V    F       V     V   F     V             V
	F  F    F       V     V   V     V             V
	======================================================
	~(p&q)<->(~p|~q) = tautology


----------

		**Nota**: algunos prefieren que la tabla anterior se mostrara así:
		::

					p  q  ~p  ~q  (p&q)  ~(p&q)  (~p|~q)  ~(p&q)<->(~p|~q)
					======================================================
					V  V   F   F    V       F       F             V
					V  F   F   V    F       V       V             V
					F  V   V   F    F       V       V             V
					F  F   V   V    F       V       V             V
					======================================================
					~(p&q)<->(~p|~q) = tautology

		Sin embargo, esta salida no muestra el estricto orden (de izquierda a derecha) de evaluación de las subexpresiones.

----------

To Do
=====

- Mejorar esta documentación
- Agregar una interfaz gráfica (GUI)
- Implementar más *features* 
- Más conectores; conectores alternativos...


License
=======

MIT License


Maintainers
===========

Written by Osmar D. Gómez A (`ozzygomez <https://github.com/ozziegomez>`_)










