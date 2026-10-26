"""Páginas internas de Franco & Asociados con head/header/footer del index.
Uso: python _scripts/generar_paginas.py   (correr DESPUÉS de generar_extras.py)
Cada página profundiza (casos, rubros, proceso, documentación, FAQ propias); no repite el index."""
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent
idx = (D / "index.html").read_text(encoding="utf8")
head_tpl = idx[:idx.index("<title>")]
links_head = idx[idx.index('<link rel="preconnect"'):idx.index("</head>")]
links_head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", links_head, flags=re.S)
links_head = re.sub(r'<meta property="og:[^>]*>\n|<meta name="twitter:[^>]*>\n', "", links_head)
top = idx[idx.index("<!-- ============ HEADER ============ -->"):idx.index("<main>")]
f0 = idx.index("<!-- ============ FOOTER ============ -->")
foot = idx[f0:idx.index('<a class="totop"', f0)]
tail = idx[idx.index('<a class="totop"', f0):]
tail = re.sub(r'<div class="modal".*?</div>\n</div>\n\n', "", tail, flags=re.S)

def interna(s):
    s = re.sub(r'href="#(?!")', 'href="./index.html#', s)
    return s.replace('href="./index.html#inicio"', 'href="./index.html"')
top, foot, tail = interna(top), interna(foot), tail.replace('href="#inicio"', 'href="#top"')

WA = 'class="btn btn-rojo js-wa" href="#"'

def page(name, title, desc, body):
    og = re.search(r'<meta property="og:image" content="([^"]+)"', idx)
    og = og.group(1) if og else "./og.png"
    meta = (f'<meta property="og:type" content="website">\n<meta property="og:locale" content="es_AR">\n'
            f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{og}">\n<meta name="twitter:card" content="summary">\n')
    html = (head_tpl + f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            '<meta name="theme-color" content="#16161A">\n<link rel="icon" type="image/png" href="./favicon.png">\n'
            '<link rel="apple-touch-icon" href="./favicon.png">\n' + meta + links_head + '</head>\n<body id="top">\n\n'
            + top + "<main>\n" + body + "\n</main>\n\n" + foot + tail)
    (D / name).write_text(html, encoding="utf8", newline="\n")
    print("ok", name)

def cabecera(eyebrow, t1, acc, ruta, bajada, foto):
    return f'''<!-- ============ CABECERA ============ -->
<section class="page-hero">
  <div class="page-hero-bg" style="background-image:linear-gradient(90deg,rgba(22,22,26,.95),rgba(22,22,26,.82) 55%,rgba(22,22,26,.55)),url(img/{foto})" aria-hidden="true"></div>
  <span class="dots dots-tl dots-on-dark" aria-hidden="true"></span>
  <span class="shard shard-br" aria-hidden="true"></span>
  <div class="wrap page-hero-in">
    <nav class="ruta" aria-label="Ruta"><a href="./index.html">Inicio</a><i class="ti ti-chevron-right" aria-hidden="true"></i><span>{ruta}</span></nav>
    <p class="eyebrow">{eyebrow}</p>
    <h1 class="page-h1">{t1} <span class="acc">{acc}</span></h1>
    <p class="page-sub">{bajada}</p>
  </div>
</section>
'''

def cards(items):
    return "".join(f'<article class="tipo reveal"><i class="ti {ic}" aria-hidden="true"></i><h3>{t}</h3><p>{p}</p></article>' for ic, t, p in items)

def lista(items):
    return "".join(f'<li><i class="ti ti-check" aria-hidden="true"></i><span><b>{t}</b>{p}</span></li>' for t, p in items)

def proceso(items):
    return "".join(f'<li class="reveal"><span class="pr-n">{i+1:02d}</span><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(items))

def faq(items):
    return "".join(f'<details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in items)

def cta_box(titulo, texto, msg):
    return f'''    <div class="cta-box reveal">
      <div><h2 class="h2">{titulo}</h2><p>{texto}</p></div>
      <div class="cta-btns">
        <a {WA} data-msg="{msg}">Consultar por WhatsApp</a>
        <a class="btn btn-line-osc" href="tel:+541160936384">Llamar</a>
      </div>
    </div>
'''

def add_cta(body, titulo, texto, msg, sola=False):
    """La CTA va dentro de la última sección (así no quedan dos fondos iguales seguidos);
    con sola=True va en su propia sección clara (cuando la última sección es oscura)."""
    box = cta_box(titulo, texto, msg)
    if sola:
        return body + '\n<section class="sec claro2 cta-int">\n  <div class="wrap">\n' + box + '  </div>\n</section>'
    i = body.rstrip().rindex('</section>')
    return body[:i] + '  <div class="wrap">\n' + box + '  </div>\n' + body[i:]

# =============== ACCIDENTES DE TRÁNSITO ===============
b = cabecera("Accidentes de tránsito", "Tu reclamo,", "de principio a fin.", "Accidentes de tránsito",
             "Si sufriste lesiones o daños en un accidente, podés reclamar a la aseguradora del responsable. Te acompañamos desde la primera consulta hasta el cierre.", "hero.jpg")
b += f'''
<section class="sec claro">
  <div class="wrap">
    <div class="sec-head reveal"><p class="divtitle"><span>Casos que atendemos</span></p><h2 class="h2">Cada accidente <span class="acc">es distinto</span></h2></div>
    <div class="tipos">{cards([
      ("ti-car-crash", "Choques entre vehículos", "Colisiones en la calle, en ruta o en intersecciones."),
      ("ti-motorbike", "Accidentes de moto", "Conductores y acompañantes, una de las situaciones más frecuentes."),
      ("ti-walk", "Peatones y ciclistas", "Si te atropellaron cruzando o circulando en bicicleta."),
      ("ti-steering-wheel", "Uber, taxi, remís y apps", "Pasajeros que se lesionaron viajando en un servicio de transporte."),
      ("ti-bus", "Transporte público", "Accidentes arriba de un colectivo o al subir o bajar."),
      ("ti-tool", "Daños al vehículo", "Reparación, pérdida total y privación de uso del auto o la moto.")])}</div>
  </div>
</section>

<section class="sec oscuro">
  <div class="foto-bg" aria-hidden="true"></div>
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Qué se puede reclamar</p>
      <h2 class="h2">Los rubros <span class="acc">de tu indemnización</span></h2>
      <p class="sub">Según cada caso, el reclamo puede incluir distintos conceptos. En la consulta analizamos cuáles corresponden al tuyo.</p>
    </div>
    <ul class="rubros reveal">{lista([
      ("Incapacidad física y psicológica", "Las secuelas que dejó el accidente."),
      ("Gastos médicos", "Atención, estudios, farmacia y kinesiología."),
      ("Lucro cesante", "Lo que dejaste de ganar mientras te recuperabas."),
      ("Daño moral", "El impacto del accidente en tu vida."),
      ("Daños materiales", "Reparación del vehículo y privación de uso."),
      ("Gastos de traslado", "Movilidad para tratamientos y trámites.")])}</ul>
  </div>
</section>

<section class="sec claro">
  <div class="wrap">
    <div class="sec-head reveal"><p class="divtitle"><span>Cómo es el reclamo</span></p><h2 class="h2">Paso a paso, <span class="acc">con vos</span></h2></div>
    <ol class="proceso">{proceso([
      ("Consulta", "Escuchamos qué pasó y analizamos tu caso."),
      ("Documentación", "Reunimos la denuncia, los certificados médicos, fotos y los datos del seguro."),
      ("Reclamo", "Presentamos el reclamo ante la aseguradora del responsable."),
      ("Mediación", "Buscamos un acuerdo antes de llegar a juicio."),
      ("Juicio", "Si no hay acuerdo, iniciamos la demanda.")])}</ol>
  </div>
</section>

<section class="sec oscuro">
  <div class="wrap split">
    <div class="aviso reveal">
      <i class="ti ti-alert-triangle" aria-hidden="true"></i>
      <h2 class="h3">Antes de aceptar una oferta</h2>
      <p>La aseguradora puede ofrecerte un monto rápido, incluso por WhatsApp. No todas las propuestas contemplan las lesiones sufridas y sus consecuencias.</p>
      <p class="aviso-caso">En un caso reciente, un pasajero de Uber recibió una oferta informal de <b>$450.000</b> y el reclamo terminó en un acuerdo de <b>$4.950.000</b>.</p>
      <p class="nota">Cada caso es distinto y no se garantizan resultados.</p>
    </div>
    <div class="reveal">
      <p class="eyebrow">Documentación útil</p>
      <h2 class="h2">Qué tener <span class="acc">a mano</span></h2>
      <ul class="docs">
        <li>DNI y datos de contacto</li><li>Datos del otro conductor y de su seguro</li><li>Denuncia del siniestro</li>
        <li>Certificados y estudios médicos</li><li>Fotos del lugar y de los vehículos</li><li>Datos de los testigos</li>
      </ul>
      <p class="plazo-txt"><i class="ti ti-hourglass" aria-hidden="true"></i>El reclamo tiene plazos: en general, tres años para la responsabilidad civil. Cuanto antes consultes, mejor.</p>
    </div>
  </div>
</section>

<section class="sec claro">
  <div class="wrap faq-wrap">
    <div class="sec-head reveal"><p class="divtitle"><span>Dudas frecuentes</span></p><h2 class="h2">Sobre accidentes <span class="acc">de tránsito</span></h2></div>
    <div class="faq reveal">{faq([
      ("Iba de acompañante. ¿Puedo reclamar?", "Sí. Los acompañantes y pasajeros también pueden reclamar por las lesiones que sufrieron."),
      ("El otro conductor no tenía seguro. ¿Qué pasa?", "Igual podés reclamar al responsable. Analizamos el caso para ver la mejor vía."),
      ("¿Cuánto tarda el reclamo?", "Depende de cada caso: si hay acuerdo en mediación es más rápido; si va a juicio, lleva más tiempo."),
      ("¿Cómo son los honorarios?", "Te los explicamos con claridad en la primera consulta, antes de iniciar cualquier trámite.")])}</div>
  </div>
</section>

'''
b = add_cta(b, "¿Tuviste un accidente?", "Contanos qué pasó y te decimos cómo seguir.", "Hola, tuve un accidente de tránsito y quisiera hacer una consulta.")
page("accidentes-de-transito.html", "Accidentes de tránsito | Franco & Asociados",
     "Reclamos por accidentes de auto, moto, peatones, ciclistas y pasajeros de Uber o colectivos. Rubros, proceso del reclamo y documentación. Franco & Asociados.", b)

# =============== ART ===============
b = cabecera("ART", "Accidentes de trabajo", "y enfermedades laborales.", "ART",
             "Si te lesionaste trabajando, en el camino al trabajo o por las tareas que hacés, la ART tiene que darte cobertura. Te representamos frente a la aseguradora.", "art.jpg")
b += f'''
<section class="sec claro">
  <div class="wrap">
    <div class="sec-head reveal"><p class="divtitle"><span>Qué cubre la ART</span></p><h2 class="h2">Situaciones <span class="acc">que atendemos</span></h2></div>
    <div class="tipos tipos-4">{cards([
      ("ti-building-factory-2", "Accidentes en el trabajo", "Lesiones ocurridas mientras realizabas tus tareas."),
      ("ti-route", "Accidentes in itinere", "En el trayecto entre tu casa y el trabajo, ida o vuelta."),
      ("ti-lungs", "Enfermedades profesionales", "Afecciones causadas por el tipo de trabajo que hacés."),
      ("ti-bandage", "Secuelas después del alta", "Si te dieron el alta y seguís con dolores o limitaciones.")])}</div>
  </div>
</section>

<section class="sec oscuro">
  <div class="foto-bg foto-art" aria-hidden="true"></div>
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Si te accidentaste</p>
      <h2 class="h2">Qué hacer <span class="acc">primero</span></h2>
      <p class="sub">Los primeros pasos cuidan tu salud y tu reclamo.</p>
    </div>
    <ul class="rubros reveal">{lista([
      ("Avisá a tu empleador", "Informá el accidente lo antes posible."),
      ("Pedí atención por la ART", "Es la aseguradora la que tiene que cubrir tu tratamiento y los traslados."),
      ("Guardá todo", "Certificados, estudios, recetas y comunicaciones."),
      ("Consultá antes de firmar", "Si te dan el alta y seguís con dolores, consultanos.")])}</ul>
  </div>
</section>

<section class="sec claro">
  <div class="wrap">
    <div class="sec-head reveal"><p class="divtitle"><span>El reclamo</span></p><h2 class="h2">Cómo <span class="acc">lo llevamos</span></h2></div>
    <ol class="proceso">{proceso([
      ("Análisis del caso", "Revisamos qué pasó, la atención recibida y tu situación laboral."),
      ("Comisión médica", "Te acompañamos en la evaluación de la incapacidad."),
      ("Reclamo a la ART", "Exigimos la cobertura y la indemnización que correspondan."),
      ("Instancia judicial", "Si la respuesta no es justa, seguimos por la vía judicial.")])}</ol>
  </div>
</section>

<section class="sec oscuro">
  <div class="wrap faq-wrap">
    <div class="sec-head reveal"><p class="divtitle"><span>Dudas frecuentes</span></p><h2 class="h2">Sobre <span class="acc">ART</span></h2></div>
    <div class="faq reveal">{faq([
      ("¿Me pueden despedir por reclamar a la ART?", "El reclamo se dirige a la aseguradora, que es la responsable de la cobertura. Reclamar no debería poner en riesgo tu empleo."),
      ("Trabajo sin registrar. ¿Tengo cobertura?", "Aunque no estés registrado, tenés derechos ante un accidente de trabajo. Consultanos y vemos tu caso."),
      ("¿Qué es un accidente in itinere?", "Es el que ocurre en el trayecto habitual entre tu casa y tu trabajo, de ida o de vuelta."),
      ("La ART me negó los traslados. ¿Puedo reclamar?", "Sí. La ART tiene que garantizar los traslados para tu tratamiento médico.")])}</div>
  </div>
</section>

'''
b = add_cta(b, "¿Te accidentaste trabajando?", "Te explicamos qué te corresponde y cómo reclamarlo.", "Hola, quisiera hacer una consulta por un accidente de trabajo / ART.", sola=True)
page("art.html", "ART y accidentes de trabajo | Franco & Asociados",
     "Accidentes de trabajo, in itinere, enfermedades profesionales y secuelas después del alta. Te representamos frente a la ART. Franco & Asociados.", b)

# =============== SUCESIONES E IMPUESTOS ===============
b = cabecera("Sucesiones e impuestos", "Ordenamos lo que", "tu familia necesita.", "Sucesiones e impuestos",
             "Te acompañamos en el trámite sucesorio y en las cuestiones impositivas, con explicaciones claras en cada paso.", "archivo.jpg")
b += f'''
<section class="sec claro">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Sucesiones</p>
      <h2 class="h2">El trámite, <span class="acc">paso a paso</span></h2>
      <p class="sub">La sucesión permite que los herederos reciban los bienes de la persona fallecida y puedan disponer de ellos.</p>
    </div>
    <ol class="proceso proceso-v reveal">{proceso([
      ("Documentación", "Partida de defunción, partidas que acrediten el vínculo y datos de los bienes."),
      ("Inicio de la sucesión", "Presentamos el pedido ante el juzgado."),
      ("Declaratoria de herederos", "El juez determina quiénes son los herederos."),
      ("Inscripción de bienes", "Se inscriben inmuebles, vehículos y cuentas a nombre de los herederos.")])}</ol>
  </div>
</section>

<section class="sec oscuro">
  <div class="foto-bg foto-arch" aria-hidden="true"></div>
  <div class="wrap faq-wrap">
    <div class="sec-head reveal"><p class="divtitle"><span>Consultas frecuentes</span></p><h2 class="h2">Sobre <span class="acc">sucesiones</span></h2></div>
    <div class="faq reveal">{faq([
      ("Un coheredero no quiere iniciar la sucesión. ¿Qué hago?", "Cualquier heredero puede iniciarla. Te explicamos cómo avanzar aunque otro no participe."),
      ("No encuentro la escritura de la propiedad. ¿Puedo seguir?", "Sí. Hay formas de obtener una copia o los datos necesarios para continuar el trámite."),
      ("¿Los nietos pueden heredar si falleció su papá o su mamá?", "Sí. Pueden heredar en representación de su padre o madre fallecidos."),
      ("¿Cuánto tarda una sucesión?", "Depende de cada caso, de la documentación disponible y del acuerdo entre herederos.")])}</div>
  </div>
</section>

<section class="sec claro" id="impuestos">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Impuestos</p>
      <h2 class="h2">Asesoramiento <span class="acc">impositivo</span></h2>
      <p class="sub">Te orientamos en tus obligaciones y en los reclamos o presentaciones que necesites hacer.</p>
    </div>
    <div class="tipos tipos-2 reveal">{cards([
      ("ti-file-invoice", "Situación impositiva", "Revisamos tu situación y te explicamos tus obligaciones."),
      ("ti-scale", "Presentaciones y reclamos", "Te representamos en trámites y reclamos ante los organismos.")])}</div>
  </div>
</section>

'''
b = add_cta(b, "¿Tenés una consulta?", "Contanos tu situación y te orientamos.", "Hola, quisiera hacer una consulta por una sucesión / impuestos.")
page("sucesiones-e-impuestos.html", "Sucesiones e impuestos | Franco & Asociados",
     "Trámite sucesorio paso a paso, declaratoria de herederos y consultas frecuentes. Asesoramiento impositivo. Franco & Asociados.", b)

# =============== NOSOTROS ===============
b = cabecera("El estudio", "Más de 50 años", "a tu lado.", "Nosotros",
             "Un estudio que acompaña a cada cliente con compromiso, experiencia y confianza.", "firma.jpg")
b += f'''
<section class="sec claro">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Quiénes somos</p>
      <h2 class="h2">Experiencia <span class="acc">que acompaña</span></h2>
      <p class="sub">Somos socios comprometidos en ayudarte. Brindamos asesoramiento y representación legal con atención personalizada y acompañamiento en cada etapa, para que obtengas la compensación que merecés.</p>
    </div>
    <div class="cifras reveal">
      <div><b>+50</b><span>años de trayectoria</span></div>
      <div><b>24 h</b><span>de atención</span></div>
      <div><b>4</b><span>áreas de práctica</span></div>
      <div><b>4</b><span>canales de contacto</span></div>
    </div>
  </div>
</section>

<section class="sec oscuro">
  <div class="wrap">
    <div class="sec-head reveal"><p class="divtitle"><span>Nuestros valores</span></p><h2 class="h2">Cómo <span class="acc">trabajamos</span></h2></div>
    <div class="tipos tipos-4">{cards([
      ("ti-heart-handshake", "Compromiso", "Tu caso es nuestro caso, desde el primer contacto."),
      ("ti-award", "Experiencia", "Más de cinco décadas de trayectoria."),
      ("ti-shield-check", "Honestidad", "Te decimos lo que podés esperar, con claridad."),
      ("ti-user-check", "Atención personalizada", "Soluciones a medida y contacto constante.")])}</div>
  </div>
</section>

<section class="sec claro">
  <div class="wrap split">
    <div class="equipo-card reveal">
      <span class="eq-ic" aria-hidden="true"><i class="ti ti-user-star"></i></span>
      <small>Directora comercial</small>
      <h3>Romina Miguel</h3>
      <p>Su dedicación y pasión se reflejan en la interacción constante con nuestros clientes, dando atención personalizada y soluciones a medida.</p>
    </div>
    <div class="reveal">
      <p class="eyebrow">Siempre disponibles</p>
      <h2 class="h2">Atención <span class="acc">las 24 horas</span></h2>
      <p class="sub">Respondemos tus consultas en todo momento, por el canal que te quede más cómodo.</p>
      <ul class="canales">
        <li><i class="ti ti-brand-whatsapp" aria-hidden="true"></i>WhatsApp</li>
        <li><i class="ti ti-phone" aria-hidden="true"></i>Teléfono</li>
        <li><i class="ti ti-mail" aria-hidden="true"></i>E-mail</li>
        <li><i class="ti ti-world" aria-hidden="true"></i>Nuestra web</li>
      </ul>
    </div>
  </div>
</section>

'''
b = add_cta(b, "Hablemos de tu caso", "Asesoría personalizada. Estamos con vos en todo el proceso.", "Hola, quisiera hacer una consulta.")
page("nosotros.html", "Nosotros | Franco & Asociados",
     "Franco & Asociados: más de 50 años de trayectoria, atención personalizada y atención las 24 horas. Conocé el estudio y cómo trabajamos.", b)
