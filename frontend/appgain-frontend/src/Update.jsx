import { useForm } from "react-hook-form";
import axios from 'axios';

export const Update = () => {

    // React form for ease of implementation
    const { register, handleSubmit } = useForm();

    // Update document based on input
    const onSubmit = async (data) => {
        let clean_data = {}
        if (data['ios_primary']){
          clean_data.ios = {primary:data['ios_primary'], fallback:data['ios_fallback']}
        }
        if (data['android_primary']){
          clean_data.android = {primary:data['android_primary'], fallback:data['android_fallback']}
        }
        if (data['web']){
          clean_data.web = data['web']
        }
        const rawResponse = await axios(`http://127.0.0.1:8000/shortlinks/${data['slug']}`, {
          method: "PUT",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          data: JSON.stringify(clean_data),
        });
      };

    return (
      <>
          <h1>Update Shortened URL</h1>
          <h3>Enter the slug of the url you would like to update, if updating IOS, you must update both primary and fallback. The same applies to Android</h3>
    <br/>
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
      </>
  )
}
