var tour=new Shepherd.Tour({defaultStepOptions:{cancelIcon:{enabled:!0},classes:"shadow-md bg-purple-dark",scrollTo:{behavior:"smooth",block:"center"}},useModalOverlay:{enabled:!0}});tour.addStep({title:"Welcome Back !",text:"This is Step 1",attachTo:{element:"#logo-tour",on:"bottom"},buttons:[{text:"Next",classes:"btn btn-success",action:tour.next}]}),tour.addStep({title:"Register your account",text:"Get your Free HIRING account now.",attachTo:{element:"#register-tour",on:"bottom"},buttons:[{text:"Back",classes:"btn btn-light",action:tour.back},{text:"Next",classes:"btn btn-success",action:tour.next}]}),tour.addStep({title:"Login your account",text:"Sign in to continue to HIRING.",attachTo:{element:"#login-tour",on:"bottom"},buttons:[{text:"Back",classes:"btn btn-light",action:tour.back},{text:"Next",classes:"btn btn-success",action:tour.next}]}),tour.addStep({title:"Get yout Product",text:"Sign in to continue to HIRING.",attachTo:{element:"#getproduct-tour",on:"bottom"},buttons:[{text:"Back",classes:"btn btn-light",action:tour.back},{text:"Next",classes:"btn btn-success",action:tour.next}]}),tour.addStep({title:"Thank you !",text:"Sign in to continue to HIRING.",attachTo:{element:"#thankyou-tour",on:"bottom"},buttons:[{text:"Back",classes:"btn btn-light",action:tour.back},{text:"Thank you !",classes:"btn btn-primary",action:tour.complete}]}),tour.start();