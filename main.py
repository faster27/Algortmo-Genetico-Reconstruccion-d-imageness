
import numpy as np
import cv2
import random
import matplotlib.pyplot as plt

class ADN():
    def __init__(self,target,mutation_rate,n_individuals,n_selection,n_generations,verbose=True):
        self.target =target
        self.n_individuals=n_individuals
        self.n_selection=n_selection
        self.mutation_rate=mutation_rate
        self.verbose=verbose
        self.n_generations=n_generations

    def create_individual(self):
        individual=np.random.randint(0, 255, (100, 100,3), np.uint8)

       ## cv2.imshow('imagen', individual)
        ##cv2.waitKey(0)
        return individual.flatten()

    def create_population(self):
        population=[self.create_individual() for i in range(self.n_individuals)]
        return population


    ##se puede mirar si se coloca que tambie sume la distacnia entre los numero
    ##del original con el generado entremas cerca este del numero real mejor es el fitness


    ##NOTA: INTENTAR APLANANDO LAS MTRIZES PARA VER SI RESULTA MAS RAPIDO
    ##SE APALAN EL INDIDUAL Y EL TARGET TAMBIEND EBE ESTAR APLANADO
    def fitness(self,individual):

        individuo=individual.flatten()
        objetivo=self.target.flatten()
        fitness=0

        Totaliguales=np.sum(individuo==objetivo)
        fitness=Totaliguales

      #  for i in range(len(individuo)):

                #if abs(individuo[i]-objetivo[i]<=5):
                   # fitness+=0.5


        print("fitness: ",fitness)
        return fitness



    ##AQUI SE USA LA SELECCION POR TORNEO
    ##EL TORNEO SACA SUBGRUPOS DE 4
    def selection(self,population):


        numeroParticipantes=4
        seleccionados=[]

        scores=[(self.fitness(i),i) for i in population]

        for i in range(self.n_selection):
           participantes = random.sample(scores, numeroParticipantes)
           participantesOrdenados=sorted(participantes,key=lambda p: p[0])

           seleccionados.append(participantesOrdenados[3][1])

          #if participantes[0][0] >participantes[1][0]:
                #seleccionados.append(participantes[0][1])
          # else:
              # seleccionados.append(participantes[1][1])

           ##NOTA AQUI CREO QUE PUEDE DAR MAS PESO QUE CUANDO SEAN IGUALES SE EVALUE CUAL TIEN VALORES MAS CERCANOS
            ##AL OBJETIVO Y EL QUE TENGA MAS ES EL QUE QUEDA

       # print(len(seleccionados))



        ##sortedScore=sorted(scores,key=lambda p: p[0])

        ##scores=[i[1] for i in sortedScore]

        ##selected=scores[len(scores)- self.n_selection:]
        return seleccionados

   ##AQUI LA REPRODUCCION SUCEDE CON EL METODO DE DOS PUNTOS
    def reproduction(self,population,selected):
        point=0
        father=[]

        for i in range(len(population)):
            punto1=np.random.randint(1,len(self.target)-1)
            punto2=np.random.randint(1,len(self.target)-1)

            while punto1 > punto2:
                punto1 = np.random.randint(1, len(self.target) - 1)
                punto2 = np.random.randint(1, len(self.target) - 1)



            father=random.sample(selected,2)

            population[i][:punto1]=father[0][:punto1]

            population[i][punto2:] = father[1][punto2:]


        return population

    def mutation(self,population):
        for i in range(len(population)):
            if random.random() <= self.mutation_rate:
                puntofila=random.randint(0,len(self.target)-1)
                puntocolumna = random.randint(0, len(self.target) - 1)
                new_value=np.random.randint(0,255)

               # if population[i][puntocolumna]!=self.target[puntocolumna]:

                while new_value==population[i][puntocolumna]:
                    new_value = np.random.randint(0, 255)

                population[i][puntocolumna]=new_value

        return population

    def run(self):
        population=self.create_population()
       ## video = cv2.VideoWriter('VideoFinal.wmv', cv2.VideoWriter_fourcc(*'mp4v'), 20, (50, 50), isColor=False)

        for i in range(self.n_generations):
            if self.verbose:
                print('______________')
                print('GENERACION: ',i)
                ##print('POBLACION: ', population)

            selected=self.selection(population)
            population=self.reproduction(population,selected)
            population=self.mutation(population)
            #video.write(population[0])
            cv2.imshow('Resultado', cv2.resize(population[0].reshape(100,100,3),(200,200),interpolation = cv2.INTER_NEAREST))
            cv2.waitKey(1)
      #  video.release()
        print(self.fitness(population[0]))

        return population[0].reshape(100,100,3)


def main():
        target=cv2.imread('PaisajeColor.jpg',1)

        cv2.imshow('Objetivo', cv2.resize(target,(200,200),interpolation = cv2.INTER_NEAREST))
        cv2.waitKey(1)

        target = target.flatten()
        model=ADN(target=target,mutation_rate=0.9,n_individuals=4000,n_selection=1000,n_generations=50000, verbose=True)
        ImagenFinal=model.run()


        ##aqui se imprime el resultado final
        cv2.imshow('Imagen final', ImagenFinal)
        cv2.waitKey(0)

if __name__ == '__main__':
    main()


















