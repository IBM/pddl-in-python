(define (problem BW-rand-5)
    (:domain blocksworld)
  (:objects b1 b2 b3 b4 b5  - block)
  (:init
   (handempty)
   (ontable b1)
   (on b2 b4)
   (on b3 b2)
   (on b4 b1)
   (ontable b5)
   (clear b3)
   (clear b5))
  (:goal
   (and
    (on b1 b5)
    (on b3 b2)
    (on b4 b3)
    (on b5 b4))))
