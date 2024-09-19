/*
 * Doki: Quantum Computer simulator, using state vectors. QSimov core.
 * Copyright (C) 2021  Hernán Indíbil de la Cruz Calvo
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

/** \file qstate.h
 *  \brief Functions and structures needed to define a quantum state.
 *
 *  In this file some functions and structures have been defined
 *  to create and destroy a quantum state vector.
 */

/** \def __QSTATE_H
 *  \brief Indicates if qstate.h has already been loaded.
 *
 *  If __QSTATE_H is defined, qstate.h file has already been included.
 */

/** \struct array_list qstate.h "qstate.h"
 *  \brief List of complex number arrays.
 *  A list of complex number arrays (chunks).
 */

#pragma once
#ifndef QSTATE_H_
#define QSTATE_H_

#include "platform.h"
#include <stdbool.h>

struct state_vector {
	/* total size of the vector */
	NATURAL_TYPE size;
	/* number of chunks */
	size_t num_chunks;
	/* number of qubits in this quantum system */
	unsigned int num_qubits;
	/* partial vector */
	COMPLEX_TYPE **vector;
	/* normalization constant */
	REAL_TYPE norm_const;
	/* fcarg initialized */
	bool fcarg_init;
	/* first complex argument */
	REAL_TYPE fcarg;
};

/** \fn unsigned char state_init(struct state_vector *this, unsigned int
 * num_qubits, int init); \brief Initialize a state vector structure. \param
 * this Pointer to an already allocated state_vector structure. \param
 * num_qubits The number of qubits represented by this state (a maximum of
 * MAX_NUM_QUBITS). \param init Whether to initialize to {1, 0, ..., 0} or not.
 *  \return 0 if ok, 1 if failed to allocate vector, 2 if failed to allocate
 * any chunk, 3 if num_qubits > MAX_NUM_QUBITS.
 */
unsigned char state_init(struct state_vector *this, unsigned int num_qubits,
			 bool init);

/** \fn unsigned char state_clone(struct state_vector *dest, struct
 * state_vector *source); \brief Clone a state vector structure. \param dest
 * Pointer to an already allocated state_vector structure i which the copy will
 * be stored. \param source Pointer to the state_vector structure that has to
 * be cloned. \return 0 if ok, 1 if failed to allocate dest vector, 2 if failed
 * to allocate any chunk.
 */
unsigned char state_clone(struct state_vector *dest,
			  struct state_vector *source);

void state_clear(struct state_vector *this);

#define state_set(this, i, value) (this)->vector[(i) / COMPLEX_ARRAY_SIZE][(i) % COMPLEX_ARRAY_SIZE] = value

#define state_get(this, i) (COMPLEX_DIV_R((this)->vector[(i) / COMPLEX_ARRAY_SIZE][(i) % COMPLEX_ARRAY_SIZE], (this)->norm_const))

size_t state_mem_size(struct state_vector *this);

#endif /* QSTATE_H_ */
