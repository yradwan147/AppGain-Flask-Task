import { useForm } from "react-hook-form";
import axios from 'axios';
import { useState } from "react";

export const Add = () => {

  // Slug and shown states to preview prototype result
  const [slug, setSlug] = useState("")
  const [shown, setShown] = useState("hidden")

  // React form for ease of implementation
  const { register, handleSubmit } = useForm();

  // Request to add new document using form data
  const onSubmit = async (data) => {
    const rawResponse = await axios("http://127.0.0.1:8000/shortlinks", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      data: JSON.stringify({
        slug: data['slug'],
        ios: {
          primary: data['ios_primary'],
          fallback: data['ios_fallback'],
        },
        android: {
          primary: data['android_primary'],
          fallback: data['android_fallback'],
        },
        web: data['web'],
      }),
    });
    setSlug(rawResponse['data']['slug'])
    setShown("visible")
  };

    return (<>
    <h1>Shorten URL</h1>
    <h3>Shorten a new URL. If no slug is added, a random one will be generated</h3>
    <form onSubmit={handleSubmit(onSubmit)}>
        <div className="form-group">
          <label>Slug (If left empty, creates random slug)</label>
          <input className="form-control" type="text" {...register("slug")} />
        </div>
        <div className="form-group">
          <label>IOS Primary Link</label>
          <input className="form-control" type="text" {...register("ios_primary")} />
        </div>
        <div className="form-group">
          <label>IOS Fallback Link</label>
          <input className="form-control" type="text" {...register("ios_fallback")} />
        </div>
        <div className="form-group">
          <label>Android Primary Link</label>
          <input className="form-control" type="text" {...register("android_primary")} />
        </div>
        <div className="form-group">
          <label>Android Fallback Link</label>
          <input className="form-control" type="text" {...register("android_fallback")} />
        </div>
        <div className="form-group">
          <label>Web Link</label>
          <input className="form-control" type="text" {...register("web")} />
        </div>
        <input className="form-control btn btn-primary " type="submit"/>
      </form>
      <br/>
      <h4 id = "result" style={{visibility:shown}}>Your new URL is http://127.0.0.1:8000/{slug}</h4>
      </>
  )
}
