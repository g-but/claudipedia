import { NextRequest, NextResponse } from 'next/server'

// Mock article data - in real app this would come from Neo4j database
const mockArticles: Record<string, any> = {
  'classical-mechanics': {
    title: 'Classical Mechanics',
    sections: [
      {
        id: 'introduction',
        title: 'Introduction',
        content: `<p>Classical mechanics is a branch of physics that deals with the motion of macroscopic objects under the influence of forces. It is one of the oldest and most fundamental branches of physics, forming the foundation for much of modern physics and engineering.</p>

<p>The development of classical mechanics can be traced back to ancient times, but its modern form was established primarily through the work of Isaac Newton in the 17th century. Newton's three laws of motion and his law of universal gravitation provided a comprehensive framework for understanding mechanical phenomena.</p>

<p>Classical mechanics is typically divided into two main areas: kinematics, which describes motion without considering its causes, and dynamics, which studies the relationship between motion and the forces that produce it.</p>`,
        level: 1
      },
      {
        id: 'newtons-laws',
        title: "Newton's Laws of Motion",
        content: `<p><strong>Newton's First Law (Law of Inertia):</strong> An object at rest stays at rest, and an object in motion stays in motion at constant velocity unless acted upon by an external force. This law describes the natural tendency of objects to resist changes in their state of motion.</p>

<p><strong>Newton's Second Law (F = ma):</strong> The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. This is expressed mathematically as <code>F = ma</code>, where F is the net force, m is the mass, and a is the acceleration.</p>

<p><strong>Newton's Third Law:</strong> For every action, there is an equal and opposite reaction. This law explains that forces always occur in pairs - if object A exerts a force on object B, object B simultaneously exerts an equal and opposite force on object A.</p>`,
        level: 1
      },
      {
        id: 'key-concepts',
        title: 'Key Concepts',
        content: `<p><strong>Mass and Inertia:</strong> Mass is a measure of an object's resistance to acceleration. Inertia is the tendency of an object to maintain its state of rest or uniform motion.</p>

<p><strong>Force:</strong> A force is any influence that causes an object to undergo a change in speed, direction, or shape. Forces can be contact forces (like friction or normal force) or field forces (like gravity or electromagnetic forces).</p>

<p><strong>Energy:</strong> The capacity to do work. In classical mechanics, energy can take several forms including kinetic energy (energy of motion) and potential energy (stored energy).</p>

<p><strong>Work and Power:</strong> Work is done when a force acts on an object and causes displacement. Power is the rate at which work is done.</p>`,
        level: 1
      },
      {
        id: 'applications',
        title: 'Applications',
        content: `<p>Classical mechanics finds applications in numerous fields:</p>
<ul>
<li><strong>Engineering:</strong> Design of machines, vehicles, structures, and mechanical systems</li>
<li><strong>Astronomy:</strong> Orbital mechanics, satellite positioning, and space mission planning</li>
<li><strong>Ballistics:</strong> Projectile motion, weapon design, and forensic analysis</li>
<li><strong>Sports:</strong> Understanding and improving athletic performance and equipment design</li>
<li><strong>Robotics:</strong> Control systems, manipulator design, and autonomous navigation</li>
<li><strong>Transportation:</strong> Vehicle dynamics, traffic flow modeling, and safety systems</li>
</ul>`,
        level: 1
      }
    ],
    lastModified: '2024-01-15',
    contributors: ['Dr. Sarah Chen', 'Prof. Michael Rodriguez', 'Claude AI'],
    confidence: 0.95,
    sources: [
      'Newton, I. (1687). Philosophiæ Naturalis Principia Mathematica.',
      'Feynman, R. P., Leighton, R. B., & Sands, M. (1963). The Feynman Lectures on Physics.',
      'Halliday, D., Resnick, R., & Walker, J. (2013). Fundamentals of Physics.',
      'Serway, R. A., & Jewett, J. W. (2018). Physics for Scientists and Engineers.'
    ]
  },
  'quantum-mechanics': {
    title: 'Quantum Mechanics',
    sections: [
      {
        id: 'introduction',
        title: 'Introduction',
        content: `<p>Quantum mechanics is a fundamental theory in physics that describes the physical properties of nature at the scale of atoms and subatomic particles. It forms the foundation of all quantum physics including quantum chemistry, quantum field theory, quantum technology, and quantum information science.</p>

<p>Classical physics, the description of physics that existed before the theory of relativity and quantum mechanics, describes many aspects of nature at an ordinary (macroscopic) scale, while quantum mechanics explains the aspects of nature at small (atomic and subatomic) scales.</p>`,
        level: 1
      },
      {
        id: 'wave-particle-duality',
        title: 'Wave-Particle Duality',
        content: `<p>One of the most fundamental concepts in quantum mechanics is wave-particle duality. This principle states that every particle or quantum entity exhibits both wave and particle properties. Light and matter display characteristics of both waves and particles, depending on the experiment performed.</p>

<p>The double-slit experiment demonstrates this duality most clearly. When particles such as electrons are fired at a barrier with two slits, they create an interference pattern characteristic of waves, yet when detectors are placed at the slits, the particles behave like discrete particles.</p>`,
        level: 1
      },
      {
        id: 'uncertainty-principle',
        title: 'Uncertainty Principle',
        content: `<p>Formulated by Werner Heisenberg in 1927, the uncertainty principle states that it is impossible to simultaneously know both the position and momentum of a particle with arbitrary precision. This is not due to limitations of measurement technology, but is a fundamental property of nature itself.</p>

<p>Mathematically, this is expressed as: <code>Δx ⋅ Δp ≥ ℏ/2</code>, where Δx is the uncertainty in position, Δp is the uncertainty in momentum, and ℏ is the reduced Planck's constant.</p>`,
        level: 1
      }
    ],
    lastModified: '2024-01-14',
    contributors: ['Dr. Lisa Park', 'Prof. David Kim', 'Claude AI'],
    confidence: 0.90,
    sources: [
      'Heisenberg, W. (1927). Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik.',
      'Bohr, N. (1913). On the Constitution of Atoms and Molecules.',
      'Dirac, P. A. M. (1958). The Principles of Quantum Mechanics.'
    ]
  },
  'theory-of-relativity': {
    title: 'Theory of Relativity',
    sections: [
      {
        id: 'introduction',
        title: 'Introduction',
        content: `<p>The theory of relativity, developed by Albert Einstein, consists of two interrelated theories: special relativity and general relativity. Special relativity applies to all physical phenomena in the absence of gravity, while general relativity provides a description of gravity as the curvature of spacetime.</p>

<p>These theories revolutionized our understanding of space, time, mass, energy, and gravity, replacing Newton's law of universal gravitation and providing the foundation for modern physics and cosmology.</p>`,
        level: 1
      },
      {
        id: 'special-relativity',
        title: 'Special Theory of Relativity',
        content: `<p>Published by Einstein in 1905, special relativity is based on two postulates:</p>

<p><strong>First Postulate:</strong> The laws of physics are the same in all inertial frames of reference.</p>

<p><strong>Second Postulate:</strong> The speed of light in vacuum is constant and independent of the motion of the source or observer.</p>

<p>From these postulates emerge several counterintuitive but experimentally verified phenomena, including time dilation, length contraction, and mass-energy equivalence (E = mc²).</p>`,
        level: 1
      }
    ],
    lastModified: '2024-01-13',
    contributors: ['Dr. Robert Martinez', 'Prof. Elena Volkov', 'Claude AI'],
    confidence: 0.98,
    sources: [
      'Einstein, A. (1905). On the Electrodynamics of Moving Bodies.',
      'Einstein, A. (1916). The Foundation of the General Theory of Relativity.',
      'Misner, C. W., Thorne, K. S., & Wheeler, J. A. (1973). Gravitation.'
    ]
  }
}

interface PageProps {
  params: {
    slug: string
  }
}

export async function GET(request: NextRequest, { params }: PageProps) {
  const article = mockArticles[params.slug]

  if (!article) {
    return NextResponse.json({ error: 'Article not found' }, { status: 404 })
  }

  return NextResponse.json(article)
}

